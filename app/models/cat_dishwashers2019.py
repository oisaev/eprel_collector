from sqlalchemy import Column, ForeignKeyConstraint, String

from .cat_base import CategoryBase


class Dishwashers2019(CategoryBase):
    '''Модель категории dishwashers2019.'''
    __table_args__ = (
        ForeignKeyConstraint(
            columns=['eprel_id', 'scraping_start_datetime'],
            refcolumns=['common.eprel_id', 'common.scraping_start_datetime'],
        ),
    )
    energyClass = Column(String(32767), nullable=True)
    energyCons100 = Column(String(32767), nullable=True)
    ratedCapacity = Column(String(32767), nullable=True)
    waterCons = Column(String(32767), nullable=True)
    programmeDuration = Column(String(32767), nullable=True)
    noise = Column(String(32767), nullable=True)
    noiseClass = Column(String(32767), nullable=True)
