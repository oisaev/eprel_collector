import asyncio

import aiohttp

from core.constants import (
    EPREL_URL_API,
    EPREL_URL_PDF,
    EPREL_URL_SHORT,
    X_API_KEY,
)
from core.logging import logger
from core.settings import settings


async def get_eprel_category_api(eprel_id):
    '''Определение категории продукта.'''
    async with aiohttp.ClientSession() as session:
        url_short = EPREL_URL_SHORT.format(eprel_id=eprel_id)
        attempts = 0
        while attempts < settings.re_read_attempts:
            try:
                async with session.get(
                    url=url_short,
                    timeout=settings.http_timeout,
                ) as response:
                    response_url = response.url
                    url_path = response_url.path.split('/')
                    if str(response_url) != url_short and len(url_path) >= 2:
                        return url_path[-2], True
            except Exception:
                logger.exception(
                    f'{eprel_id=}, attempt {attempts+1}. '
                    f'Failed to convert url_short->url_long'
                )
            attempts += 1
            await asyncio.sleep(settings.pause_between_attempts)
        return None, False


async def get_dict_from_json_api(eprel_id, eprel_category):
    '''Получение словаря со всеми значениями атрибутов продукта из json.'''
    async with aiohttp.ClientSession() as session:
        url_api = EPREL_URL_API.format(
            eprel_category=eprel_category, eprel_id=eprel_id
        )
        attempts = 0
        while attempts < settings.re_read_attempts:
            try:
                async with session.get(
                    url=url_api,
                    headers={'x-api-key': X_API_KEY},
                    timeout=settings.http_timeout,
                ) as response:
                    dict_from_json = await response.json()
                    if dict_from_json:
                        return dict_from_json, True
            except Exception:
                logger.exception(
                    f'{eprel_id=}, attempt {attempts+1}. '
                    f'Failed to get API response'
                )
            attempts += 1
            await asyncio.sleep(settings.pause_between_attempts)
    return None, False


async def get_pdfs_zip_api(eprel_id, eprel_category):
    '''Получение архива с PDF файлами fiche на всех языках.'''
    async with aiohttp.ClientSession() as session:
        url_pdf = EPREL_URL_PDF.format(
            eprel_category=eprel_category, eprel_id=eprel_id
        )
        attempts = 0
        while attempts < settings.re_read_attempts:
            try:
                async with session.get(
                    url=url_pdf,
                    headers={'x-api-key': X_API_KEY},
                    timeout=settings.http_timeout,
                ) as response:
                    file_name = response.url.path.split('/')[-1]
                    fiche = await response.read()
                    if len(fiche) > 5000:
                        return fiche, file_name, True
            except Exception:
                logger.exception(
                    f'{eprel_id=}, attempt {attempts+1}. '
                    f'Failed to get fiches zip'
                )
            attempts += 1
            await asyncio.sleep(settings.pause_between_attempts)
    return None, None, False
