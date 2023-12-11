from datetime import datetime

from sqlalchemy import and_, or_, select

from core.db import AsyncSessionLocal
from core.logging import logger
from core.settings import settings
from models import Common, PDFCommit, ValueChangeLog


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


async def get_already_collected_pdfs():
    '''Получение списка продуктов, для которых не надо собирать PDF файлы.'''
    async with AsyncSessionLocal() as session:
        date_time = await session.execute(
            select(
                PDFCommit.pdf_commit_datetime
            ).select_from(
                PDFCommit
            ).order_by(
                PDFCommit.pdf_commit_datetime.desc()
            ).limit(1)
        )
    date_time = date_time.scalar()
    if not date_time:
        date_time = datetime.fromisoformat('1000-01-01')
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
                or_(
                    Common.eprel_category_status != 'parsing',
                    and_(
                        Common.eprel_category_status == 'parsing',
                        Common.scraping_datetime <= date_time
                    )
                )
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


async def pdf_commit(date_time):
    try:
        date_time = datetime.fromisoformat(date_time)
    except ValueError:
        logger.warning('PDF commit: time format is wrong')
    else:
        new_record = PDFCommit()
        new_record.pdf_commit_datetime = date_time
        async with AsyncSessionLocal() as session:
            session.add(new_record)
            await session.commit()
        logger.info(f'PDF commit: added {date_time} commit')
