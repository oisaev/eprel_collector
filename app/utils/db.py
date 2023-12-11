from datetime import datetime

from sqlalchemy import and_, delete, select

from core.db import AsyncSessionLocal
from core.settings import settings
from models import Common, PDFCommit, ValueChangeLog
from utils.value_from_json import value_json


async def get_item_by_eprel_id_db_model(eprel_id, db_model):
    '''
    Получение экземпляра модели по eprel_id и модели:
    - если запись с таким eprel_id уже есть, возвращает эту запись
    - если записи с таким eprel_id нет, возвращает пустой экземпляр.
    '''
    async with AsyncSessionLocal() as session:
        item = await session.execute(
            select(
                db_model
            ).select_from(
                db_model
            ).where(
                db_model.eprel_id == eprel_id
            )
        )
    item = item.first()
    item = item[0] if item else None
    if not item:
        item = db_model()
    return item


async def get_already_collected(category_statuses):
    '''Получение списка собранных продуктов в определенных статусах.'''
    async with AsyncSessionLocal() as session:
        products = await session.execute(
            select(
                Common.eprel_id
            ).select_from(
                Common
            ).where(
                Common.eprel_id.between(
                    settings.eprel_id_min,
                    settings.eprel_id_max
                )
            ).where(
                Common.eprel_category_status.in_(category_statuses)
            )
        )
    products = products.scalars().all()
    return set(products)


async def get_n_th_datetime_pdf_commit(position):
    async with AsyncSessionLocal() as session:
        date_time = await session.execute(
            select(
                PDFCommit.pdf_commit_datetime
            ).select_from(
                PDFCommit
            ).order_by(
                PDFCommit.pdf_commit_datetime.desc()
            ).limit(
                1
            ).offset(
                position-1
            )
        )
    return date_time.scalar()


async def get_eprel_ids_to_collect_pdfs_db(from_dt, to_dt):
    '''Получение списка продуктов, для которых надо собирать PDF файлы.'''
    async with AsyncSessionLocal() as session:
        products = await session.execute(
            select(
                Common.eprel_id
            ).select_from(
                Common
            ).where(
                Common.eprel_id.between(
                    settings.eprel_id_min,
                    settings.eprel_id_max
                )
            ).where(
                and_(
                    Common.eprel_category_status == 'parsing',
                    Common.scraping_datetime >= from_dt,
                    Common.scraping_datetime <= to_dt,
                )
            )
        )
    products = products.scalars().all()
    return set(products)


async def save_product_db(
    eprel_id, eprel_category, dict_from_json, common_item, attrs_item
):
    '''Запись информации о продукте в БД.'''
    previous_scraping_datetime = common_item.scraping_datetime
    current_scraping_datetime = datetime.now()
    common_item.eprel_id = eprel_id
    common_item.scraping_datetime = current_scraping_datetime
    common_item.eprel_category = eprel_category
    common_item.eprel_category_status = 'parsing'
    common_item.eprel_manufacturer = value_json(
        dict_from_json, settings.eprel_manufacturer_attr
    )
    common_item.eprel_model_identifier = value_json(
        dict_from_json, settings.eprel_model_identifier_attr
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

    attrs = settings.category_to_scrap[eprel_category]
    for attribute_name in attrs:
        previous_value = getattr(attrs_item, attribute_name)
        current_value = value_json(dict_from_json, attribute_name)
        if attrs_item.eprel_id and previous_value != current_value:
            await save_value_change_log(
                eprel_id,
                eprel_category,
                attribute_name,
                previous_scraping_datetime,
                previous_value,
                current_scraping_datetime,
                current_value
            )
        setattr(attrs_item, attribute_name, current_value)
    attrs_item.eprel_id = eprel_id

    async with AsyncSessionLocal() as session:
        session.add(common_item)
        await session.commit()
        session.add(attrs_item)
        await session.commit()


async def save_value_change_log(
    eprel_id,
    eprel_category,
    attribute_name,
    previous_scraping_datetime,
    previous_value,
    current_scraping_datetime,
    current_value
):
    '''Запись в лог изменения значения аттрибута.'''
    new_record_db = ValueChangeLog()
    new_record_db.eprel_id = eprel_id
    new_record_db.eprel_category = eprel_category
    new_record_db.attribute_name = attribute_name
    new_record_db.previous_scraping_datetime = previous_scraping_datetime
    new_record_db.previous_value = previous_value
    new_record_db.current_scraping_datetime = current_scraping_datetime
    new_record_db.current_value = current_value
    async with AsyncSessionLocal() as session:
        session.add(new_record_db)
        await session.commit()


async def save_non_parsing_db(
    eprel_id, eprel_category, eprel_category_status
):
    '''
    Если не собираем атрибуты - просто записываем
    продукт в "лог" (только модель Common).
    '''
    common_item = await get_item_by_eprel_id_db_model(eprel_id, Common)
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


async def save_pdf_commit(date_time):
    new_record = PDFCommit()
    new_record.pdf_commit_datetime = date_time
    async with AsyncSessionLocal() as session:
        session.add(new_record)
        await session.commit()


async def remove_pdf_commits(number_of_commits):
    commits = await get_pdf_commit_list(number_of_commits)
    async with AsyncSessionLocal() as session:
        await session.execute(
            delete(
                PDFCommit
            ).where(
                PDFCommit.pdf_commit_datetime.in_(commits)
            )
        )
        await session.commit()
        return len(commits)


async def get_pdf_commit_list(number_of_commits):
    async with AsyncSessionLocal() as session:
        commits = await session.execute(
            select(
                PDFCommit.pdf_commit_datetime
            ).select_from(
                PDFCommit
            ).order_by(
                PDFCommit.pdf_commit_datetime.desc()
            ).limit(number_of_commits)
        )
    return commits.scalars().all()
