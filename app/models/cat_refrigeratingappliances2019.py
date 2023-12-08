from sqlalchemy import Column, ForeignKeyConstraint, String

from .models_base import IdTimeBase


class Refrigeratingappliances2019(IdTimeBase):
    '''Модель категории refrigeratingappliances2019.'''
    __table_args__ = (
        ForeignKeyConstraint(
            columns=['eprel_id', 'scraping_start_datetime'],
            refcolumns=['common.eprel_id', 'common.scraping_start_datetime'],
        ),
    )
    energyClass = Column(String(32767), nullable=True)
    energyConsAnnual = Column(String(32767), nullable=True)
    consolidatedEnergyConsAnnual = Column(String(32767), nullable=True)
    capFreezeNet = Column(String(32767), nullable=True)
    capRefrNet = Column(String(32767), nullable=True)
    capBottles = Column(String(32767), nullable=True)
    noise = Column(String(32767), nullable=True)
    noiseClass = Column(String(32767), nullable=True)
    totalVolume = Column(String(32767), nullable=True)
