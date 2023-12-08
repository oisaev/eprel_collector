from sqlalchemy import Column, DateTime, Integer

from core.db import Base


class CategoryBase(Base):
    '''Базовая модель для категорий.'''
    __abstract__ = True

    eprel_id = Column(Integer, nullable=False)
    scraping_start_datetime = Column(DateTime, nullable=False)
