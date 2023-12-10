from sqlalchemy import select

from core.db import AsyncSessionLocal
from core.settings import settings
from models import Common


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


async def get_already_collected():
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
            )
        )
    products = products.scalars().all()
    return set(products)
