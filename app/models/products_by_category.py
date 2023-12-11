from sqlalchemy import Column, ForeignKeyConstraint, String

from models.models_base import EprelIdBase


class Dishwashers2019(EprelIdBase):
    '''Модель категории dishwashers2019.'''
    __table_args__ = (
        ForeignKeyConstraint(
            columns=['eprel_id'],
            refcolumns=['common.eprel_id'],
        ),
    )
    energyClass = Column(String(32767), nullable=False)
    energyCons100 = Column(String(32767), nullable=False)
    ratedCapacity = Column(String(32767), nullable=False)
    waterCons = Column(String(32767), nullable=False)
    programmeDuration = Column(String(32767), nullable=False)
    noise = Column(String(32767), nullable=False)
    noiseClass = Column(String(32767), nullable=False)


class Electronicdisplays(EprelIdBase):
    '''Модель категории electronicdisplays.'''
    __table_args__ = (
        ForeignKeyConstraint(
            columns=['eprel_id'],
            refcolumns=['common.eprel_id'],
        ),
    )
    energyClassSDR = Column(String(32767), nullable=False)
    powerOnModeSDR = Column(String(32767), nullable=False)
    energyClassHDR = Column(String(32767), nullable=False)
    powerOnModeHDR = Column(String(32767), nullable=False)
    resolutionHorizontalPixels = Column(String(32767), nullable=False)
    resolutionVerticalPixels = Column(String(32767), nullable=False)
    diagonalCm = Column(String(32767), nullable=False)
    diagonalInch = Column(String(32767), nullable=False)
    panelTechnology = Column(String(32767), nullable=False)


class Lightsources(EprelIdBase):
    '''Модель категории lightsources.'''
    __table_args__ = (
        ForeignKeyConstraint(
            columns=['eprel_id'],
            refcolumns=['common.eprel_id'],
        ),
    )
    energyClass = Column(String(32767), nullable=False)
    powerOnMode = Column(String(32767), nullable=False)
    energyConsOnMode = Column(String(32767), nullable=False)


class Refrigeratingappliances2019(EprelIdBase):
    '''Модель категории refrigeratingappliances2019.'''
    __table_args__ = (
        ForeignKeyConstraint(
            columns=['eprel_id'],
            refcolumns=['common.eprel_id'],
        ),
    )
    energyClass = Column(String(32767), nullable=False)
    energyConsAnnual = Column(String(32767), nullable=False)
    consolidatedEnergyConsAnnual = Column(String(32767), nullable=False)
    capFreezeNet = Column(String(32767), nullable=False)
    capRefrNet = Column(String(32767), nullable=False)
    capBottles = Column(String(32767), nullable=False)
    noise = Column(String(32767), nullable=False)
    noiseClass = Column(String(32767), nullable=False)
    totalVolume = Column(String(32767), nullable=False)


class Tyres(EprelIdBase):
    '''Модель категории tyres.'''
    __table_args__ = (
        ForeignKeyConstraint(
            columns=['eprel_id'],
            refcolumns=['common.eprel_id'],
        ),
    )
    sizeDesignation = Column(String(32767), nullable=False)
    tyreDesignation = Column(String(32767), nullable=False)
    loadCapacityIndex = Column(String(32767), nullable=False)
    loadCapacityIndex2 = Column(String(32767), nullable=False)
    loadCapacityIndex3 = Column(String(32767), nullable=False)
    loadCapacityIndex4 = Column(String(32767), nullable=False)
    speedCategorySymbol = Column(String(32767), nullable=False)
    speedCategorySymbol2 = Column(String(32767), nullable=False)
    loadCapacityIndicator = Column(String(32767), nullable=False)
    tyreClass = Column(String(32767), nullable=False)
    energyClass = Column(String(32767), nullable=False)
    wetGripClass = Column(String(32767), nullable=False)
    externalRollingNoiseValue = Column(String(32767), nullable=False)
    externalRollingNoiseClass = Column(String(32767), nullable=False)
    severeSnowTyre = Column(String(32767), nullable=False)
    iceTyre = Column(String(32767), nullable=False)


class Washerdriers2019(EprelIdBase):
    '''Модель категории washerdriers2019.'''
    __table_args__ = (
        ForeignKeyConstraint(
            columns=['eprel_id'],
            refcolumns=['common.eprel_id'],
        ),
    )
    energyClassWashAndDry = Column(String(32767), nullable=False)
    energyClassWash = Column(String(32767), nullable=False)
    energyConsumption100WashAndDry = Column(String(32767), nullable=False)
    energyConsumption100Wash = Column(String(32767), nullable=False)
    ratedCapacityWashAndDry = Column(String(32767), nullable=False)
    ratedCapacityWash = Column(String(32767), nullable=False)
    waterConsumptionWashAndDry = Column(String(32767), nullable=False)
    waterConsumptionWash = Column(String(32767), nullable=False)
    programDurationRatedWashAndDry = Column(String(32767), nullable=False)
    programDurationRatedWash = Column(String(32767), nullable=False)
    spinClass = Column(String(32767), nullable=False)
    noise = Column(String(32767), nullable=False)
    noiseClass = Column(String(32767), nullable=False)


class Washingmachines2019(EprelIdBase):
    '''Модель категории washingmachines2019.'''
    __table_args__ = (
        ForeignKeyConstraint(
            columns=['eprel_id'],
            refcolumns=['common.eprel_id'],
        ),
    )
    energyClass = Column(String(32767), nullable=False)
    energyConsPerCycle = Column(String(32767), nullable=False)
    energyConsPer100Cycle = Column(String(32767), nullable=False)
    ratedCapacity = Column(String(32767), nullable=False)
    programmeDurationRated = Column(String(32767), nullable=False)
    waterCons = Column(String(32767), nullable=False)
    spinClass = Column(String(32767), nullable=False)
    noise = Column(String(32767), nullable=False)
    noiseClass = Column(String(32767), nullable=False)
