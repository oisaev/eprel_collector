from sqlalchemy import Column, DateTime, String

from models.models_base import EprelIdBase


class ValueChangeLog(EprelIdBase):
    '''Модель записи изменений в значениях атрибутов.'''

    eprel_category = Column(String(255), nullable=False)
    attribute_name = Column(String(255), nullable=False)
    previous_scraping_datetime = Column(DateTime, nullable=False)
    previous_value = Column(String(32767), nullable=False)
    current_scraping_datetime = Column(DateTime, nullable=False)
    current_value = Column(String(32767), nullable=False)
