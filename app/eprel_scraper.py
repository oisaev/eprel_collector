import asyncio
import datetime
import re

import aiohttp

from core.db import AsyncSessionLocal
from core.logging import logger  # noqa
from core.settings import settings
import models


def eprel_id_generator():
    for id in range(settings.eprel_id_min, settings.eprel_id_max+1):
        yield id


async def get_eprel_category(session, eprel_id):
    url_short = settings.eprel_url_shart.format(eprel_id=eprel_id)
    async with session.get(
        url=url_short,
        timeout=settings.http_timeout,
    ) as response:
        url_path = response.url.path.split('/')
        if len(url_path) >= 2:
            return response.url.path.split('/')[-2]
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


async def save_common_info(
    scraping_start_datetime, eprel_id, eprel_category, api_json_dict
):
    info = models.Common()
    info.eprel_id = eprel_id
    info.scraping_start_datetime = scraping_start_datetime
    info.eprel_category = eprel_category
    info.eprel_manufacturer = value_json(
        api_json_dict, 'supplierOrTrademark'
    )
    info.eprel_model_identifier = value_json(
        api_json_dict, 'modelIdentifier'
    )
    info.eprel_url_short = settings.eprel_url_shart.format(eprel_id=eprel_id)
    info.eprel_url_long = settings.eprel_url_long.format(
        eprel_category=eprel_category, eprel_id=eprel_id
    )
    info.eprel_url_api = settings.eprel_url_api.format(
        eprel_category=eprel_category, eprel_id=eprel_id
    )
    async with AsyncSessionLocal() as session:
        session.add(info)
        await session.commit()


async def save_category_info(
    scraping_start_datetime, eprel_id, eprel_category, api_json_dict
):
    pass


async def scrap_eprel_id(
    scraping_start_datetime, session, eprel_id, eprel_category
):
    url_api = settings.eprel_url_api.format(
        eprel_category=eprel_category, eprel_id=eprel_id
    )
    async with session.get(
        url=url_api,
        headers={'x-api-key': settings.x_api_key},
        timeout=settings.http_timeout,
    ) as response:
        api_json_dict = await response.json()
    logger.info(f'{eprel_id=} {eprel_category=} has downloaded')
    await save_common_info(
        scraping_start_datetime, eprel_id, eprel_category, api_json_dict
    )
    await save_category_info(
        scraping_start_datetime, eprel_id, eprel_category, api_json_dict
    )


async def gather_eprel(scraping_start_datetime, get_eprel_id):
    for eprel_id in get_eprel_id:
        async with aiohttp.ClientSession() as session:
            eprel_category = await get_eprel_category(session, eprel_id)
            if not eprel_category:
                pass
            elif eprel_category in settings.category_exceptional:
                pass
            elif eprel_category == settings.category_error:
                pass
            elif eprel_category not in settings.category_to_scrap:
                pass
            else:
                await scrap_eprel_id(
                    scraping_start_datetime, session, eprel_id, eprel_category
                )


async def main():
    scraping_start_datetime = datetime.datetime.now()
    get_eprel_id = eprel_id_generator()
    tasks = []
    for _ in range(settings.eprel_maximum_connections+1):
        tasks.append(
            asyncio.create_task(
                gather_eprel(scraping_start_datetime, get_eprel_id)
            )
        )
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
