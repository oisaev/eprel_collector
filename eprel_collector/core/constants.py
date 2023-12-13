X_API_KEY = '3PR31D3F4ULTU1K3Y2020'

EPREL_URL_SHORT = 'https://eprel.ec.europa.eu/qr/{eprel_id}'

EPREL_URL_LONG = (
    'https://eprel.ec.europa.eu/screen/product/{eprel_category}/{eprel_id}'
)

EPREL_URL_API = (
    'https://eprel.ec.europa.eu/api/products/{eprel_category}/{eprel_id}'
)

EPREL_URL_PDF = (
    'https://eprel.ec.europa.eu/api/products/'
    '{eprel_category}/{eprel_id}/fiches'
)

EPREL_MANUFACTURER_ATTR = 'supplierOrTrademark'

EPREL_MODEL_IDENTIFIER_ATTR = 'modelIdentifier'

CATEGORY_NOT_RELEASED = 'error'

CATEGORY_NON_PARSING = (
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

CATEGORY_PARSING = {
    'dishwashers2019': (
        'energyClass',
        'energyCons100',
        'ratedCapacity',
        'waterCons',
        'programmeDuration',
        'noise',
        'noiseClass',
    ),
    'electronicdisplays': (
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
    'lightsources': (
        'energyClass',
        'powerOnMode',
        'energyConsOnMode',
    ),
    'refrigeratingappliances2019': (
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
    'tyres': (
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
    'washerdriers2019': (
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
    'washingmachines2019': (
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

CATEGORY_STATUS = {
    'parsing': 'Category to parse attributes',
    'non_parsing': 'Category is an non-parsing one',
    'not_released': 'Product is not released yet',
    'new': 'Newly appeared category',
    'broken': 'Broken product, url_short->url_long conversion error',
}
CATEGORY_STATUS_LIST = [(key, value) for key, value in CATEGORY_STATUS.items()]
