from datetime import datetime

from core.arg_parser import command_line_args
from core.settings import settings
from utils.db import (
    get_already_collected_products_db,
    get_eprel_ids_to_collect_pdfs_db,
    get_n_th_datetime_pdf_commit_db,
)


async def get_eprel_ids():
    '''Создание списка id для сбора продуктов либо PDF fiche продуктов.'''
    if command_line_args.mode == 'pdf':
        return await get_eprel_ids_to_collect_pdfs()
    eprel_ids = set(range(settings.eprel_id_min, settings.eprel_id_max + 1))
    already_collected = set()
    if command_line_args.mode == 'remaining':
        already_collected = await get_already_collected_products_db(
            ('parsing', 'non_parsing', 'not_released')
        )
    elif command_line_args.mode == 'not_collected':
        already_collected = await get_already_collected_products_db(
            ('parsing', 'non_parsing')
        )
    return eprel_ids.difference(already_collected)


async def get_eprel_ids_to_collect_pdfs():
    '''Создание списка id для сбора PDF fiche продуктов.'''
    if command_line_args.pdf_commit_from:
        from_dt = (
            await get_n_th_datetime_pdf_commit_db(
                command_line_args.pdf_commit_from
            )
            or datetime.min
        )
    else:
        from_dt = await get_n_th_datetime_pdf_commit_db(1) or datetime.min
    if command_line_args.pdf_commit_to:
        to_dt = (
            await get_n_th_datetime_pdf_commit_db(
                command_line_args.pdf_commit_to
            )
            or datetime.min
        )
    else:
        to_dt = datetime.max
    if not (from_dt == to_dt == datetime.min):
        return await get_eprel_ids_to_collect_pdfs_db(from_dt, to_dt)
    return set()
