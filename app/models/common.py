from sqlalchemy import Column, DateTime, Integer, String, UniqueConstraint
from sqlalchemy_utils import URLType

from core.db import Base


class Common(Base):
    '''Модель основной информации о продуктах.'''
    __table_args__ = (
        UniqueConstraint(
            'eprel_id',
            'scraping_start_datetime',
            name="unique_eprel_id_scraping_start_datetime"
        ),
    )

    eprel_id = Column(Integer, nullable=False)
    scraping_start_datetime = Column(DateTime, nullable=False)
    eprel_category = Column(String(255), nullable=True)
    eprel_manufacturer = Column(String(255), nullable=True)
    eprel_model_identifier = Column(String(32767), nullable=True)
    eprel_url_short = Column(URLType, nullable=False)
    eprel_url_long = Column(URLType, nullable=True)
    eprel_url_api = Column(URLType, nullable=True)
