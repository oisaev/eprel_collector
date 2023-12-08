from sqlalchemy import Column, ForeignKeyConstraint, String

from .models_base import IdTimeBase


class Washingmachines2019(IdTimeBase):
    '''Модель категории washingmachines2019.'''
    __table_args__ = (
        ForeignKeyConstraint(
            columns=['eprel_id', 'scraping_start_datetime'],
            refcolumns=['common.eprel_id', 'common.scraping_start_datetime'],
        ),
    )
    energyClass = Column(String(32767), nullable=True)
    energyConsPerCycle = Column(String(32767), nullable=True)
    energyConsPer100Cycle = Column(String(32767), nullable=True)
    ratedCapacity = Column(String(32767), nullable=True)
    programmeDurationRated = Column(String(32767), nullable=True)
    waterCons = Column(String(32767), nullable=True)
    spinClass = Column(String(32767), nullable=True)
    noise = Column(String(32767), nullable=True)
    noiseClass = Column(String(32767), nullable=True)
