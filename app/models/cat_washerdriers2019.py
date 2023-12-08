from sqlalchemy import Column, ForeignKeyConstraint, String

from .cat_base import CategoryBase


class Washerdriers2019(CategoryBase):
    '''Модель категории washerdriers2019.'''
    __table_args__ = (
        ForeignKeyConstraint(
            columns=['eprel_id', 'scraping_start_datetime'],
            refcolumns=['common.eprel_id', 'common.scraping_start_datetime'],
        ),
    )
    energyClassWashAndDry = Column(String(32767), nullable=True)
    energyClassWash = Column(String(32767), nullable=True)
    energyConsumption100WashAndDry = Column(String(32767), nullable=True)
    energyConsumption100Wash = Column(String(32767), nullable=True)
    ratedCapacityWashAndDry = Column(String(32767), nullable=True)
    ratedCapacityWash = Column(String(32767), nullable=True)
    waterConsumptionWashAndDry = Column(String(32767), nullable=True)
    waterConsumptionWash = Column(String(32767), nullable=True)
    programDurationRatedWashAndDry = Column(String(32767), nullable=True)
    programDurationRatedWash = Column(String(32767), nullable=True)
    spinClass = Column(String(32767), nullable=True)
    noise = Column(String(32767), nullable=True)
    noiseClass = Column(String(32767), nullable=True)
