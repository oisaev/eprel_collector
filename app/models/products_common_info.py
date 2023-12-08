from sqlalchemy import Column, DateTime, Integer, String, UniqueConstraint
from sqlalchemy_utils import ChoiceType, URLType

from core.db import Base


CATEGORY_STATUSES = [
    ('parsing', 'Category to parse attributes'),
    ('exception', 'Exceptional category'),
    ('new', 'Newly appeared category'),
    ('not_released', 'Product is not released yet'),
    ('broken', 'Broken product, url_short -> url_long conversion error'),
]


class Common(Base):
    '''Модель основной информации о продуктах.'''
    __table_args__ = (
        UniqueConstraint(
            'eprel_id',
            name="unique_eprel_id"
        ),
    )

    eprel_id = Column(Integer, nullable=False)
    scraping_start_datetime = Column(DateTime, nullable=False)
    eprel_category = Column(String(255), nullable=True)
    eprel_category_status = Column(
        ChoiceType(CATEGORY_STATUSES), nullable=False
    )
    eprel_manufacturer = Column(String(255), nullable=True)
    eprel_model_identifier = Column(String(32767), nullable=True)
    eprel_url_short = Column(URLType, nullable=False)
    eprel_url_long = Column(URLType, nullable=True)
    eprel_url_api = Column(URLType, nullable=True)
