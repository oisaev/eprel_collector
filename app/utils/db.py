from datetime import datetime

from sqlalchemy import select

from core.db import AsyncSessionLocal
from core.settings import settings
from models import Common, ValueChangeLog


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


async def log_save(
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
