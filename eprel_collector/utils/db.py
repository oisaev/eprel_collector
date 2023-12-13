from datetime import datetime

from sqlalchemy import and_, delete, select

from core.constants import (
    CATEGORY_PARSING,
    EPREL_MANUFACTURER_ATTR,
    EPREL_MODEL_IDENTIFIER_ATTR,
    EPREL_URL_API,
    EPREL_URL_LONG,
    EPREL_URL_SHORT,
)
from core.db import AsyncSessionLocal
from core.settings import settings
from models import Common, PDFCommit, ValueChangeLog
from utils.value_from_json import value_json


async def get_instance_by_eprel_id_and_model_db(eprel_id, db_model):
    '''
    Получение экземпляра модели по eprel_id и модели:
    - если запись с таким eprel_id уже есть, возвращает эту запись
    - если записи с таким eprel_id нет, возвращает пустой экземпляр.
    '''
    async with AsyncSessionLocal() as session:
        instance = await session.execute(
            select(db_model)
            .select_from(db_model)
            .where(db_model.eprel_id == eprel_id)
        )
    instance = instance.first()
    instance = instance[0] if instance else None
    if not instance:
        instance = db_model()
    return instance


async def get_already_collected_products_db(category_statuses):
    '''Получение списка собранных продуктов в определенных статусах.'''
    async with AsyncSessionLocal() as session:
        products = await session.execute(
            select(Common.eprel_id)
            .select_from(Common)
            .where(
                Common.eprel_id.between(
                    settings.eprel_id_min, settings.eprel_id_max
                )
            )
            .where(Common.eprel_category_status.in_(category_statuses))
        )
    products = products.scalars().all()
    return set(products)


async def get_eprel_ids_to_collect_pdfs_db(from_dt, to_dt):
    '''Получение списка продуктов, для которых надо собирать PDF файлы.'''
    async with AsyncSessionLocal() as session:
        products = await session.execute(
            select(Common.eprel_id)
            .select_from(Common)
            .where(
                Common.eprel_id.between(
                    settings.eprel_id_min, settings.eprel_id_max
                )
            )
            .where(
                and_(
                    Common.eprel_category_status == 'parsing',
                    Common.scraping_datetime >= from_dt,
                    Common.scraping_datetime <= to_dt,
                )
            )
        )
    products = products.scalars().all()
    return set(products)


async def get_eprel_category_by_eprel_id_db(eprel_id):
    '''Получение eprel_category по eprel_id из БД.'''
    async with AsyncSessionLocal() as session:
        eprel_category = await session.execute(
            select(Common.eprel_category)
            .select_from(Common)
            .where(Common.eprel_id == eprel_id)
        )
    return eprel_category.scalar()


async def save_non_parsing_product_db(
    eprel_id, eprel_category, eprel_category_status
):
    '''Запись информации о не-parsing продукте в БД (только модель Common).'''
    common_item = await get_instance_by_eprel_id_and_model_db(eprel_id, Common)
    common_item.eprel_id = eprel_id
    common_item.scraping_datetime = datetime.now()
    common_item.eprel_category = eprel_category
    common_item.eprel_category_status = eprel_category_status
    common_item.eprel_url_short = EPREL_URL_SHORT.format(eprel_id=eprel_id)
    async with AsyncSessionLocal() as session:
        session.add(common_item)
        await session.commit()


async def save_parsing_product_db(
    eprel_id, eprel_category, dict_from_json, common_item, attrs_item
):
    '''
    Запись информации о parsing продукте в БД
    (и модель Common и модель продукта).
    '''
    previous_scraping_datetime = common_item.scraping_datetime
    current_scraping_datetime = datetime.now()
    common_item.eprel_id = eprel_id
    common_item.scraping_datetime = current_scraping_datetime
    common_item.eprel_category = eprel_category
    common_item.eprel_category_status = 'parsing'
    common_item.eprel_manufacturer = value_json(
        dict_from_json, EPREL_MANUFACTURER_ATTR
    )
    common_item.eprel_model_identifier = value_json(
        dict_from_json, EPREL_MODEL_IDENTIFIER_ATTR
    )
    common_item.eprel_url_short = EPREL_URL_SHORT.format(eprel_id=eprel_id)
    common_item.eprel_url_long = EPREL_URL_LONG.format(
        eprel_category=eprel_category, eprel_id=eprel_id
    )
    common_item.eprel_url_api = EPREL_URL_API.format(
        eprel_category=eprel_category, eprel_id=eprel_id
    )

    attrs = CATEGORY_PARSING[eprel_category]
    for attribute_name in attrs:
        previous_value = getattr(attrs_item, attribute_name)
        current_value = value_json(dict_from_json, attribute_name)
        if attrs_item.eprel_id and previous_value != current_value:
            await save_value_change_log_db(
                eprel_id,
                eprel_category,
                attribute_name,
                previous_scraping_datetime,
                previous_value,
                current_scraping_datetime,
                current_value,
            )
        setattr(attrs_item, attribute_name, current_value)
    attrs_item.eprel_id = eprel_id

    async with AsyncSessionLocal() as session:
        session.add(common_item)
        await session.commit()
        session.add(attrs_item)
        await session.commit()


async def save_value_change_log_db(
    eprel_id,
    eprel_category,
    attribute_name,
    previous_scraping_datetime,
    previous_value,
    current_scraping_datetime,
    current_value,
):
    '''
    Запись в лог (модель ValueChangeLog) информации
    об изменении значения аттрибута.
    '''
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


async def get_n_th_datetime_pdf_commit_db(position):
    '''Получение datetime n-ного PDF commit'a.'''
    async with AsyncSessionLocal() as session:
        date_time = await session.execute(
            select(PDFCommit.pdf_commit_datetime)
            .select_from(PDFCommit)
            .order_by(PDFCommit.pdf_commit_datetime.desc())
            .limit(1)
            .offset(position - 1)
        )
    return date_time.scalar()


async def save_pdf_commit_db(date_time):
    '''Запись PDF commit'а в БД.'''
    new_record = PDFCommit()
    new_record.pdf_commit_datetime = date_time
    async with AsyncSessionLocal() as session:
        session.add(new_record)
        await session.commit()


async def remove_pdf_commits_db(number_of_commits):
    '''Удаление n PDF commit'ов из БД.'''
    commits = await get_pdf_commit_list_db(number_of_commits)
    async with AsyncSessionLocal() as session:
        await session.execute(
            delete(PDFCommit).where(PDFCommit.pdf_commit_datetime.in_(commits))
        )
        await session.commit()
        return len(commits)


async def get_pdf_commit_list_db(number_of_commits):
    '''Получение списка PDF commit'ов из БД.'''
    async with AsyncSessionLocal() as session:
        commits = await session.execute(
            select(PDFCommit.pdf_commit_datetime)
            .select_from(PDFCommit)
            .order_by(PDFCommit.pdf_commit_datetime.desc())
            .limit(number_of_commits)
        )
    return commits.scalars().all()
