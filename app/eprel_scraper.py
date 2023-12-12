import asyncio
import os
import random
from datetime import datetime
from pathlib import Path

import models
from core.arg_parser import command_line_args
from core.constants import (
    CATEGORY_NON_PARSING,
    CATEGORY_NOT_RELEASED,
    CATEGORY_PARSING,
    CATEGORY_STATUS,
)
from core.logging import logger
from core.settings import settings
from utils.api import (
    get_dict_from_json_api,
    get_eprel_category_api,
    get_pdfs_zip_api,
)
from utils.db import (
    get_eprel_category_by_eprel_id_db,
    get_instance_by_eprel_id_and_model_db,
    save_non_parsing_product_db,
    save_parsing_product_db,
)
from utils.get_eprel_ids import get_eprel_ids
from utils.pdf_commits import (
    check_from_to_args_correctness,
    pdf_commit_handler,
)


def eprel_id_generator(eprel_ids):
    '''Генератор eprel_id из подготовленного списка продуктов.'''
    eprel_ids = random.sample(tuple(eprel_ids), len(eprel_ids))
    logged_persent = 0
    for yielded, eprel_id in enumerate(eprel_ids):
        yield eprel_id
        current_persent = int(100 * (yielded + 1) / len(eprel_ids))
        if current_persent > logged_persent:
            logger.info(
                f'{current_persent}% of products processed. '
                f'{yielded+1} of {len(eprel_ids)}'
            )
            logged_persent = current_persent


async def scrap_product_with_attrs(eprel_id, eprel_category):
    '''Сбор продукта вместе с атрибутами.'''
    dict_from_json, success = await get_dict_from_json_api(
        eprel_id, eprel_category
    )
    if success:
        common_item = await get_instance_by_eprel_id_and_model_db(
            eprel_id, models.Common
        )
        attrs_item = await get_instance_by_eprel_id_and_model_db(
            eprel_id, eval(f'models.{eprel_category.capitalize()}')
        )
        await save_parsing_product_db(
            eprel_id, eprel_category, dict_from_json, common_item, attrs_item
        )
        return True
    return False


async def gather_fiches(eprel_id, eprel_category):
    '''Сбор .zip архивов с .pdf fiche.'''
    fiche, fiche_url_path, success = await get_pdfs_zip_api(
        eprel_id, eprel_category
    )
    if success:
        pdfs_path = Path(settings.pdfs_dir)
        if not os.path.exists(pdfs_path):
            os.makedirs(pdfs_path)
        with open(
            os.path.join(pdfs_path, fiche_url_path.split('/')[-1]), 'wb'
        ) as f:
            f.write(fiche)
        return True
    return False


async def gather_all(get_eprel_id):
    '''
    Начало сбора, определение категории, вызов соответствующего ей обработчика.
    '''
    for eprel_id in get_eprel_id:
        if command_line_args.mode == 'pdf':
            eprel_category = await get_eprel_category_by_eprel_id_db(eprel_id)
            await gather_fiches(eprel_id, eprel_category)
        else:
            eprel_category, success = await get_eprel_category_api(eprel_id)
            if not success:
                status = 'broken'
                await save_non_parsing_product_db(eprel_id, None, status)
                logger.warning(f'{eprel_id=}. ' f'{CATEGORY_STATUS[status]}')
            elif eprel_category in CATEGORY_NON_PARSING:
                status = 'non_parsing'
                await save_non_parsing_product_db(
                    eprel_id, eprel_category, status
                )
            elif eprel_category == CATEGORY_NOT_RELEASED:
                status = 'not_released'
                await save_non_parsing_product_db(eprel_id, None, status)
            elif eprel_category not in CATEGORY_PARSING:
                status = 'new'
                await save_non_parsing_product_db(
                    eprel_id, eprel_category, status
                )
                logger.warning(
                    f'{eprel_id=} {eprel_category=}. '
                    f'{CATEGORY_STATUS[status]}'
                )
            elif not await scrap_product_with_attrs(eprel_id, eprel_category):
                logger.warning(
                    f'{eprel_id=} {eprel_category=} ' f'has not processed'
                )


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
        logger.info(
            f"Working in '{command_line_args.mode}' mode using "
            f"{settings.eprel_maximum_connections} connections"
        )
        eprel_ids = await get_eprel_ids()
        logger.info(f'Will be collected {len(eprel_ids)} products')
        get_eprel_id = eprel_id_generator(eprel_ids)
        tasks = []
        for _ in range(settings.eprel_maximum_connections + 1):
            tasks.append(asyncio.create_task(gather_all(get_eprel_id)))
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    logger.info(f'Started at {datetime.now()}')
    asyncio.run(main())
    logger.info(f'Finished at {datetime.now()}')
