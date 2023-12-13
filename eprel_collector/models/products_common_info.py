from sqlalchemy import Column, DateTime, String, UniqueConstraint
from sqlalchemy_utils import ChoiceType, URLType

from core.constants import CATEGORY_STATUS_LIST
from models.models_base import EprelIdBase


class Common(EprelIdBase):
    '''Модель основной информации о продуктах.'''

    __table_args__ = (UniqueConstraint('eprel_id', name="unique_eprel_id"),)

    scraping_datetime = Column(DateTime, nullable=False)
    eprel_category = Column(String(255), nullable=True)
    eprel_category_status = Column(
        ChoiceType(CATEGORY_STATUS_LIST), nullable=False
    )
    eprel_manufacturer = Column(String(255), nullable=True)
    eprel_model_identifier = Column(String(32767), nullable=True)
    eprel_url_short = Column(URLType, nullable=False)
    eprel_url_long = Column(URLType, nullable=True)
    eprel_url_api = Column(URLType, nullable=True)
