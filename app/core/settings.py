from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    database_url: str
    eprel_maximum_connections: int = 5
    eprel_id_min: int = 356460
    eprel_id_max: int = 1300000
    eprel_url_shart: str = 'https://eprel.ec.europa.eu/qr/{eprel_id}'
    eprel_url_long: str = (
        'https://eprel.ec.europa.eu/screen/product/{eprel_category}/{eprel_id}'
    )
    eprel_url_api: str = (
        'https://eprel.ec.europa.eu/api/products/{eprel_category}/{eprel_id}'
    )
    category_error: str = 'error'
    category_exceptional: tuple = (
        'airconditioners',
        'dishwashers',
        'hotwaterstoragetanks',
        'lamps',
        'localspaceheaters',
        'ovens',
        'professionalrefrigeratedstoragecabinets',
        'rangehoods',
        'refrigeratingappliances',
        'refrigeratingappliancesdirectsalesfunction',
        'residentialventilationunits',
        'solidfuelboilerpackages',
        'solidfuelboilers',
        'spaceheaterpackages',
        'spaceheaters',
        'spaceheatersolardevice',
        'spaceheatertemperaturecontrol',
        'televisions',
        'tumbledriers',
        'washerdriers',
        'washingmachines',
        'waterheaterpackages',
        'waterheaters',
        'waterheatersolardevices',
    )
    category_to_scrap: dict = {
        'dishwashers2019':
            (
                'energyClass',
                'energyCons100',
                'ratedCapacity',
                'waterCons',
                'programmeDuration',
                'noise',
                'noiseClass',
            ),

        'electronicdisplays':
            (
                'energyClassSDR',
                'powerOnModeSDR',
                'energyClassHDR',
                'powerOnModeHDR',
                'resolutionHorizontalPixels',
                'resolutionVerticalPixels',
                'diagonalCm',
                'diagonalInch',
                'panelTechnology',
            ),

        'lightsources':
            (
                'energyClass',
                'powerOnMode',
                'energyConsOnMode',
            ),

        'refrigeratingappliances2019':
            (
                'energyClass',
                'energyConsAnnual',
                'consolidatedEnergyConsAnnual',
                'capFreezeNet',
                'capRefrNet',
                'capBottles',
                'noise',
                'noiseClass',
                'totalVolume',
            ),

        'tyres':
            (
                'sizeDesignation',
                'tyreDesignation',
                'loadCapacityIndex',
                'loadCapacityIndex2',
                'loadCapacityIndex3',
                'loadCapacityIndex4',
                'speedCategorySymbol',
                'speedCategorySymbol2',
                'loadCapacityIndicator',
                'tyreClass',
                'energyClass',
                'wetGripClass',
                'externalRollingNoiseValue',
                'externalRollingNoiseClass',
                'severeSnowTyre',
                'iceTyre',
            ),

        'washerdriers2019':
            (
                'energyClassWashAndDry',
                'energyClassWash',
                'energyConsumption100WashAndDry',
                'energyConsumption100Wash',
                'ratedCapacityWashAndDry',
                'ratedCapacityWash',
                'waterConsumptionWashAndDry',
                'waterConsumptionWash',
                'programDurationRatedWashAndDry',
                'programDurationRatedWash',
                'spinClass',
                'noise',
                'noiseClass',
            ),

        'washingmachines2019':
            (
                'energyClass',
                'energyConsPerCycle',
                'energyConsPer100Cycle',
                'ratedCapacity',
                'programmeDurationRated',
                'waterCons',
                'spinClass',
                'noise',
                'noiseClass',
            ),
    }

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        extra = 'ignore'


settings = Settings()