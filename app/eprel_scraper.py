import asyncio
import os
import random
from datetime import datetime
from pathlib import Path

import models
from core.arg_parser import command_line_args
from core.logging import logger
from core.settings import settings
from utils.api import (
    get_dict_from_json_api,
    get_eprel_category_api,
    get_pdfs_zip_api,
)
from utils.db import (
    get_item_by_eprel_id_db_model,
    save_non_parsing_db,
    save_product_db,
)
from utils.get_eprel_ids import get_eprel_ids
from utils.pdf_commits import pdf_commit_handler


def eprel_id_generator(eprel_ids):
    '''Генератор eprel_id из подготовленного списка продуктов.'''
    to_log = {}
    if len(eprel_ids) > 500:
        for persent in range(1, 101):
            to_log[int(len(eprel_ids) / 100 * persent)] = persent
    eprel_ids = random.sample(tuple(eprel_ids), len(eprel_ids))
    for yielded, eprel_id in enumerate(eprel_ids):
        yield eprel_id
        if yielded + 1 in to_log:
            logger.info(
                f'{to_log[yielded+1]}% of products processed. '
                f'{yielded+1} of {len(eprel_ids)}'
            )


async def scrap_eprel_id_with_attrs(eprel_id, eprel_category):
    '''Сбор продукта вместе с атрибутами.'''
    dict_from_json = await get_dict_from_json_api(eprel_id, eprel_category)
    if dict_from_json:
        common_item = await get_item_by_eprel_id_db_model(
            eprel_id, models.Common
        )
        attrs_item = await get_item_by_eprel_id_db_model(
            eprel_id, eval(f'models.{eprel_category.capitalize()}')
        )
        await save_product_db(
            eprel_id, eprel_category, dict_from_json, common_item, attrs_item
        )
        return True
    return False


async def load_pdfs(eprel_id, eprel_category):
    '''Сбор архивов с .pdf fiche.'''
    fiche, fiche_url_path = await get_pdfs_zip_api(eprel_id, eprel_category)
    if len(fiche) >= 5000:
        pdfs_path = Path(settings.pdfs_dir)
        if not os.path.exists(pdfs_path):
            os.makedirs(pdfs_path)
        with open(
            os.path.join(pdfs_path, fiche_url_path.split('/')[-1]), 'wb'
        ) as f:
            f.write(fiche)
        return True
    return False


async def gather_eprel(get_eprel_id):
    '''
    Начало сбора, определение категории, вызов соответствующего ей обработчика.
    '''
    for eprel_id in get_eprel_id:
        eprel_category = await get_eprel_category_api(eprel_id)
        if command_line_args.mode == 'pdf':
            await load_pdfs(eprel_id, eprel_category)
            return
        if not eprel_category:
            status = 'broken'
            await save_non_parsing_db(eprel_id, eprel_category, status)
            logger.warning(
                f'{eprel_id=}. '
                f'{models.products_common_info.CATEGORY_STATUS[status]}'
            )
        elif eprel_category in settings.category_exceptional:
            status = 'exception'
            await save_non_parsing_db(eprel_id, eprel_category, status)
        elif eprel_category == settings.category_not_released:
            status = 'not_released'
            await save_non_parsing_db(eprel_id, None, status)
        elif eprel_category not in settings.category_to_scrap:
            status = 'new'
            await save_non_parsing_db(eprel_id, eprel_category, status)
            logger.warning(
                f'{eprel_id=} {eprel_category=}. '
                f'{models.products_common_info.CATEGORY_STATUS[status]}'
            )
        elif not await scrap_eprel_id_with_attrs(eprel_id, eprel_category):
            logger.warning(f'{eprel_id=} {eprel_category=} has not processed')


async def check_from_to_args_correctness():
    from_val = command_line_args.pdf_commit_from
    to_val = command_line_args.pdf_commit_to
    if (
        from_val is not None or to_val is not None
    ) and command_line_args.mode != 'pdf':
        logger.warning(
            'pdf_commit_from and pdf_commit_to arguments should be used only '
            'with pdf mode'
        )
    elif (from_val is not None and from_val < 1) or (
        to_val is not None and to_val < 1
    ):
        logger.warning('pdf_commit_from/pdf_commit_to should be >= 1')
    elif from_val is None and to_val is not None:
        logger.warning("pdf_commit_to can't be without pdf_commit_from")
    elif from_val is not None and to_val is not None and from_val < to_val:
        logger.warning('pdf_commit_from should be >= pdf_commit_to')
    else:
        return True


async def main():
    '''
    Работа с PDF commit'ами и запуск сбора информации через
    заданное максимальное количество соединений.
    '''
    if (
        command_line_args.pdf_commit is not None
        or command_line_args.pdf_commit_remove is not None
        or command_line_args.pdf_commit_list is not None
    ):
        await pdf_commit_handler()
    else:
        if not await check_from_to_args_correctness():
            return
        logger.info(f"Working in '{command_line_args.mode}' mode")
        eprel_ids = await get_eprel_ids()
        logger.info(f'Will be collected {len(eprel_ids)} products')
        get_eprel_id = eprel_id_generator(eprel_ids)
        tasks = []
        for _ in range(settings.eprel_maximum_connections + 1):
            tasks.append(asyncio.create_task(gather_eprel(get_eprel_id)))
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    logger.info(f'Started at {datetime.now()}')
    asyncio.run(main())
    logger.info(f'Finished at {datetime.now()}')
