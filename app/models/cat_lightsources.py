from sqlalchemy import Column, ForeignKeyConstraint, String

from .models_base import IdTimeBase


class Lightsources(IdTimeBase):
    '''Модель категории lightsources.'''
    __table_args__ = (
        ForeignKeyConstraint(
            columns=['eprel_id', 'scraping_start_datetime'],
            refcolumns=['common.eprel_id', 'common.scraping_start_datetime'],
        ),
    )
    energyClass = Column(String(32767), nullable=True)
    powerOnMode = Column(String(32767), nullable=True)
    energyConsOnMode = Column(String(32767), nullable=True)
