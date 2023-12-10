import asyncio
import re
from datetime import datetime

import aiohttp

import models
from core.db import AsyncSessionLocal
from core.logging import logger
from core.settings import settings
from utils.db import get_item_by_eprel_id_db_model


def eprel_id_generator(eprel_ids):
    for eprel_id in eprel_ids:
        yield eprel_id


async def get_eprel_category(session, eprel_id):
    url_short = settings.eprel_url_shart.format(eprel_id=eprel_id)
    attempts = 0
    while attempts < settings.re_read_attempts:
        try:
            async with session.get(
                url=url_short,
                timeout=settings.http_timeout,
            ) as response:
                response_url = response.url
                url_path = response_url.path.split('/')
                if response_url != url_short and len(url_path) >= 2:
                    return url_path[-2]
        except Exception:
            pass
        attempts += 1
        await asyncio.sleep(settings.pause_between_attempts)
    return None


def get_internal_value(key, value, attr_to_capture):
    internal_value = ''
    if type(value) in (dict, list):
        internal_value = value_json(value, attr_to_capture, key)
    elif key == attr_to_capture:
        internal_value = str(value)
    internal_value = re.sub('\t|  ', ' ', internal_value).strip()
    internal_value = internal_value if internal_value != 'None' else '-'
    return f'{internal_value} | ' if internal_value != '' else ''


def value_json(find_in, attr_to_capture, called_key=''):
    return_value = ''
    if isinstance(find_in, dict):
        for key, value in find_in.items():
            return_value += get_internal_value(
                key, value, attr_to_capture
            )
    elif isinstance(find_in, list):
        for list_item in find_in:
            return_value += get_internal_value(
                called_key, list_item, attr_to_capture
            )
    return return_value[:-3] if return_value else ''


async def save_items(
    eprel_id, eprel_category, api_json_dict, common_item, attrs_item
):
    common_item.eprel_id = eprel_id
    common_item.scraping_datetime = datetime.now()
    common_item.eprel_category = eprel_category
    common_item.eprel_category_status = 'parsing'
    common_item.eprel_manufacturer = value_json(
        api_json_dict, settings.eprel_manufacturer_attr
    )
    common_item.eprel_model_identifier = value_json(
        api_json_dict, settings.eprel_model_identifier_attr
    )
    common_item.eprel_url_short = settings.eprel_url_shart.format(
        eprel_id=eprel_id
    )
    common_item.eprel_url_long = settings.eprel_url_long.format(
        eprel_category=eprel_category, eprel_id=eprel_id
    )
    common_item.eprel_url_api = settings.eprel_url_api.format(
        eprel_category=eprel_category, eprel_id=eprel_id
    )

    attrs_item.eprel_id = eprel_id
    attrs = settings.category_to_scrap[eprel_category]
    for attr in attrs:
        setattr(attrs_item, attr, value_json(api_json_dict, attr))

    async with AsyncSessionLocal() as session:
        session.add(common_item)
        session.add(attrs_item)
        await session.commit()


async def scrap_eprel_id(
    session, eprel_id, eprel_category
):
    url_api = settings.eprel_url_api.format(
        eprel_category=eprel_category, eprel_id=eprel_id
    )
    attempts = 0
    while attempts < settings.re_read_attempts:
        try:
            async with session.get(
                url=url_api,
                headers={'x-api-key': settings.x_api_key},
                timeout=settings.http_timeout,
            ) as response:
                api_json_dict = await response.json()
            if api_json_dict:
                common_item = await get_item_by_eprel_id_db_model(
                    eprel_id, models.Common
                )
                attrs_item = await get_item_by_eprel_id_db_model(
                    eprel_id,
                    eval(f'models.{eprel_category.capitalize()}')
                )
                await save_items(
                    eprel_id,
                    eprel_category,
                    api_json_dict,
                    common_item,
                    attrs_item
                )
                logger.info(
                    f'{eprel_id=} {eprel_category=} '
                    f'has downloaded and processed'
                )
                return
        except Exception:
            pass
        attempts += 1
        await asyncio.sleep(settings.pause_between_attempts)


async def log_save(
    eprel_id, eprel_category, eprel_category_status
):
    '''Если не собираем атрибуты - просто записываем продукт в лог.'''
    common_item = await get_item_by_eprel_id_db_model(eprel_id, models.Common)
    common_item.eprel_id = eprel_id
    common_item.scraping_datetime = datetime.now()
    common_item.eprel_category = eprel_category
    common_item.eprel_category_status = eprel_category_status
    common_item.eprel_url_short = settings.eprel_url_shart.format(
        eprel_id=eprel_id
    )
    async with AsyncSessionLocal() as session:
        session.add(common_item)
        await session.commit()


async def gather_eprel(get_eprel_id):
    '''Начало сбора, определение категории.'''
    for eprel_id in get_eprel_id:
        async with aiohttp.ClientSession() as session:
            eprel_category = await get_eprel_category(session, eprel_id)
            if not eprel_category:
                status = 'broken'
                await log_save(eprel_id, eprel_category, status)
                logger.warning(
                    f'{eprel_id=}. '
                    f'{models.products_common_info.CATEGORY_STATUS[status]}.'
                )
            elif eprel_category in settings.category_exceptional:
                status = 'exception'
                await log_save(eprel_id, eprel_category, status)
                logger.info(
                    f'{eprel_id=} {eprel_category=}. '
                    f'{models.products_common_info.CATEGORY_STATUS[status]}.'
                )
            elif eprel_category == settings.category_not_released:
                status = 'not_released'
                await log_save(eprel_id, None, status)
                logger.info(
                    f'{eprel_id=}. '
                    f'{models.products_common_info.CATEGORY_STATUS[status]}.'
                )
            elif eprel_category not in settings.category_to_scrap:
                status = 'new'
                await log_save(eprel_id, eprel_category, status)
                logger.info(
                    f'{eprel_id=} {eprel_category=}. '
                    f'{models.products_common_info.CATEGORY_STATUS[status]}.'
                )
            else:
                await scrap_eprel_id(session, eprel_id, eprel_category)


async def get_eprel_ids():
    '''Создание списка продуктов, которые будут собраны.'''
    eprel_ids = set(range(settings.eprel_id_min, settings.eprel_id_max+1))
    return eprel_ids


async def main():
    '''
    Запуск сбора информации через заданное
    максимальное количество соединений.
    '''
    eprel_ids = await get_eprel_ids()
    get_eprel_id = eprel_id_generator(eprel_ids)
    tasks = []
    for _ in range(settings.eprel_maximum_connections+1):
        tasks.append(
            asyncio.create_task(
                gather_eprel(get_eprel_id)
            )
        )
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    logger.info(f'Program is started at {datetime.now()}')
    asyncio.run(main())
    logger.info(f'Program is finished at {datetime.now()}')
