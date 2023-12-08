from sqlalchemy import Column, ForeignKeyConstraint, String

from .cat_base import CategoryBase


class Tyres(CategoryBase):
    '''Модель категории tyres.'''
    __table_args__ = (
        ForeignKeyConstraint(
            columns=['eprel_id', 'scraping_start_datetime'],
            refcolumns=['common.eprel_id', 'common.scraping_start_datetime'],
        ),
    )
    sizeDesignation = Column(String(32767), nullable=True)
    tyreDesignation = Column(String(32767), nullable=True)
    loadCapacityIndex = Column(String(32767), nullable=True)
    loadCapacityIndex2 = Column(String(32767), nullable=True)
    loadCapacityIndex3 = Column(String(32767), nullable=True)
    loadCapacityIndex4 = Column(String(32767), nullable=True)
    speedCategorySymbol = Column(String(32767), nullable=True)
    speedCategorySymbol2 = Column(String(32767), nullable=True)
    loadCapacityIndicator = Column(String(32767), nullable=True)
    tyreClass = Column(String(32767), nullable=True)
    energyClass = Column(String(32767), nullable=True)
    wetGripClass = Column(String(32767), nullable=True)
    externalRollingNoiseValue = Column(String(32767), nullable=True)
    externalRollingNoiseClass = Column(String(32767), nullable=True)
    severeSnowTyre = Column(String(32767), nullable=True)
    iceTyre = Column(String(32767), nullable=True)
