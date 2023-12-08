from sqlalchemy import Column, ForeignKeyConstraint, String

from .cat_base import CategoryBase


class Electronicdisplays(CategoryBase):
    '''Модель категории electronicdisplays.'''
    __table_args__ = (
        ForeignKeyConstraint(
            columns=['eprel_id', 'scraping_start_datetime'],
            refcolumns=['common.eprel_id', 'common.scraping_start_datetime'],
        ),
    )
    energyClassSDR = Column(String(32767), nullable=True)
    powerOnModeSDR = Column(String(32767), nullable=True)
    energyClassHDR = Column(String(32767), nullable=True)
    powerOnModeHDR = Column(String(32767), nullable=True)
    resolutionHorizontalPixels = Column(String(32767), nullable=True)
    resolutionVerticalPixels = Column(String(32767), nullable=True)
    diagonalCm = Column(String(32767), nullable=True)
    diagonalInch = Column(String(32767), nullable=True)
    panelTechnology = Column(String(32767), nullable=True)
