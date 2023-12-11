from sqlalchemy import Column, DateTime, String, UniqueConstraint
from sqlalchemy_utils import ChoiceType, URLType

from models.models_base import EprelIdBase


CATEGORY_STATUS = {
    'parsing': 'Category to parse attributes',
    'exception': 'Category is an exceptional one',
    'not_released': 'Product is not released yet',
    'new': 'Newly appeared category',
    'broken': 'Broken product, url_short->url_long conversion error',
}

categoty_status_list = [(key, value) for key, value in CATEGORY_STATUS.items()]


class Common(EprelIdBase):
    '''Модель основной информации о продуктах.'''

    __table_args__ = (UniqueConstraint('eprel_id', name="unique_eprel_id"),)

    scraping_datetime = Column(DateTime, nullable=False)
    eprel_category = Column(String(255), nullable=True)
    eprel_category_status = Column(
        ChoiceType(categoty_status_list), nullable=False
    )
    eprel_manufacturer = Column(String(255), nullable=True)
    eprel_model_identifier = Column(String(32767), nullable=True)
    eprel_url_short = Column(URLType, nullable=False)
    eprel_url_long = Column(URLType, nullable=True)
    eprel_url_api = Column(URLType, nullable=True)
