from sqlalchemy import Column, Integer

from core.db import Base


class EprelIdBase(Base):
    '''Базовая модель c eprel_id.'''

    __abstract__ = True

    eprel_id = Column(Integer, nullable=False)
