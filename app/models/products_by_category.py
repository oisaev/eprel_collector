from sqlalchemy import Column, ForeignKeyConstraint, String

from .models_base import EprelIdBase


class Dishwashers2019(EprelIdBase):
    '''Модель категории dishwashers2019.'''
    __table_args__ = (
        ForeignKeyConstraint(
            columns=['eprel_id'],
            refcolumns=['common.eprel_id'],
        ),
    )
    energyClass = Column(String(32767), nullable=True)
    energyCons100 = Column(String(32767), nullable=True)
    ratedCapacity = Column(String(32767), nullable=True)
    waterCons = Column(String(32767), nullable=True)
    programmeDuration = Column(String(32767), nullable=True)
    noise = Column(String(32767), nullable=True)
    noiseClass = Column(String(32767), nullable=True)


class Electronicdisplays(EprelIdBase):
    '''Модель категории electronicdisplays.'''
    __table_args__ = (
        ForeignKeyConstraint(
            columns=['eprel_id'],
            refcolumns=['common.eprel_id'],
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


class Lightsources(EprelIdBase):
    '''Модель категории lightsources.'''
    __table_args__ = (
        ForeignKeyConstraint(
            columns=['eprel_id'],
            refcolumns=['common.eprel_id'],
        ),
    )
    energyClass = Column(String(32767), nullable=True)
    powerOnMode = Column(String(32767), nullable=True)
    energyConsOnMode = Column(String(32767), nullable=True)


class Refrigeratingappliances2019(EprelIdBase):
    '''Модель категории refrigeratingappliances2019.'''
    __table_args__ = (
        ForeignKeyConstraint(
            columns=['eprel_id'],
            refcolumns=['common.eprel_id'],
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


class Tyres(EprelIdBase):
    '''Модель категории tyres.'''
    __table_args__ = (
        ForeignKeyConstraint(
            columns=['eprel_id'],
            refcolumns=['common.eprel_id'],
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


class Washerdriers2019(EprelIdBase):
    '''Модель категории washerdriers2019.'''
    __table_args__ = (
        ForeignKeyConstraint(
            columns=['eprel_id'],
            refcolumns=['common.eprel_id'],
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


class Washingmachines2019(EprelIdBase):
    '''Модель категории washingmachines2019.'''
    __table_args__ = (
        ForeignKeyConstraint(
            columns=['eprel_id'],
            refcolumns=['common.eprel_id'],
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
