from sqlalchemy import select

from core.db import AsyncSessionLocal


async def get_item_by_eprel_id_db_model(eprel_id, db_model):
    async with AsyncSessionLocal() as session:
        common_item = await session.execute(
            select(
                db_model
            ).select_from(
                db_model
            ).where(
                db_model.eprel_id == eprel_id
            )
        )
    common_item = common_item.first()
    common_item = common_item[0] if common_item else None
    if not common_item:
        common_item = db_model()
    return common_item
