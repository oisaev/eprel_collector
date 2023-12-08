from sqlalchemy import Column, DateTime, Integer, String

from core.db import Base


class IdTimeBase(Base):
    '''Базовая модель c eprel_id и scraping_start_datetime.'''
    __abstract__ = True

    eprel_id = Column(Integer, nullable=False)
    scraping_start_datetime = Column(DateTime, nullable=False)


class ListModelBase(IdTimeBase):
    '''Базовая модель для списков продуктов с категорией.'''
    __abstract__ = True

    eprel_category = Column(String(255), nullable=True)
