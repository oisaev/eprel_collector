from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    database_url: str
    logging_dir: str = str(BASE_DIR / 'logs')
    pdfs_dir: str = str(BASE_DIR / 'pdfs')
    eprel_maximum_connections: int = 100
    eprel_id_min: int = 1
    eprel_id_max: int = 2_000_000
    re_read_attempts: int = 5
    pause_between_attempts: int = 4
    http_timeout: int = 30
    x_api_key: str = '3PR31D3F4ULTU1K3Y2020'
    eprel_url_shart: str = 'https://eprel.ec.europa.eu/qr/{eprel_id}'
    eprel_url_long: str = (
        'https://eprel.ec.europa.eu/screen/product/{eprel_category}/{eprel_id}'
    )
    eprel_url_api: str = (
        'https://eprel.ec.europa.eu/api/products/{eprel_category}/{eprel_id}'
    )
    eprel_url_pdf: str = (
        'https://eprel.ec.europa.eu/api/products/{eprel_category}/{eprel_id}/fiches'  # noqa
    )
    eprel_manufacturer_attr: str = 'supplierOrTrademark'
    eprel_model_identifier_attr: str = 'modelIdentifier'
    category_not_released: str = 'error'
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
