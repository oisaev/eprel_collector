"""First migration

Revision ID: 082e7edfc445
Revises:
Create Date: 2023-12-10 14:00:32.689443

"""
from typing import Sequence, Union

import sqlalchemy as sa
import sqlalchemy_utils
from alembic import op

from models.products_common_info import categoty_status_list


# revision identifiers, used by Alembic.
revision: str = '082e7edfc445'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('common',
    sa.Column('scraping_datetime', sa.DateTime(), nullable=False),
    sa.Column('eprel_category', sa.String(length=255), nullable=True),
    sa.Column('eprel_category_status', sqlalchemy_utils.types.choice.ChoiceType(categoty_status_list), nullable=False),
    sa.Column('eprel_manufacturer', sa.String(length=255), nullable=True),
    sa.Column('eprel_model_identifier', sa.String(length=32767), nullable=True),
    sa.Column('eprel_url_short', sqlalchemy_utils.types.url.URLType(), nullable=False),
    sa.Column('eprel_url_long', sqlalchemy_utils.types.url.URLType(), nullable=True),
    sa.Column('eprel_url_api', sqlalchemy_utils.types.url.URLType(), nullable=True),
    sa.Column('eprel_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('eprel_id', name='unique_eprel_id')
    )
    op.create_table('dishwashers2019',
    sa.Column('energyClass', sa.String(length=32767), nullable=True),
    sa.Column('energyCons100', sa.String(length=32767), nullable=True),
    sa.Column('ratedCapacity', sa.String(length=32767), nullable=True),
    sa.Column('waterCons', sa.String(length=32767), nullable=True),
    sa.Column('programmeDuration', sa.String(length=32767), nullable=True),
    sa.Column('noise', sa.String(length=32767), nullable=True),
    sa.Column('noiseClass', sa.String(length=32767), nullable=True),
    sa.Column('eprel_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['eprel_id'], ['common.eprel_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('electronicdisplays',
    sa.Column('energyClassSDR', sa.String(length=32767), nullable=True),
    sa.Column('powerOnModeSDR', sa.String(length=32767), nullable=True),
    sa.Column('energyClassHDR', sa.String(length=32767), nullable=True),
    sa.Column('powerOnModeHDR', sa.String(length=32767), nullable=True),
    sa.Column('resolutionHorizontalPixels', sa.String(length=32767), nullable=True),
    sa.Column('resolutionVerticalPixels', sa.String(length=32767), nullable=True),
    sa.Column('diagonalCm', sa.String(length=32767), nullable=True),
    sa.Column('diagonalInch', sa.String(length=32767), nullable=True),
    sa.Column('panelTechnology', sa.String(length=32767), nullable=True),
    sa.Column('eprel_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['eprel_id'], ['common.eprel_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('lightsources',
    sa.Column('energyClass', sa.String(length=32767), nullable=True),
    sa.Column('powerOnMode', sa.String(length=32767), nullable=True),
    sa.Column('energyConsOnMode', sa.String(length=32767), nullable=True),
    sa.Column('eprel_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['eprel_id'], ['common.eprel_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('refrigeratingappliances2019',
    sa.Column('energyClass', sa.String(length=32767), nullable=True),
    sa.Column('energyConsAnnual', sa.String(length=32767), nullable=True),
    sa.Column('consolidatedEnergyConsAnnual', sa.String(length=32767), nullable=True),
    sa.Column('capFreezeNet', sa.String(length=32767), nullable=True),
    sa.Column('capRefrNet', sa.String(length=32767), nullable=True),
    sa.Column('capBottles', sa.String(length=32767), nullable=True),
    sa.Column('noise', sa.String(length=32767), nullable=True),
    sa.Column('noiseClass', sa.String(length=32767), nullable=True),
    sa.Column('totalVolume', sa.String(length=32767), nullable=True),
    sa.Column('eprel_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['eprel_id'], ['common.eprel_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tyres',
    sa.Column('sizeDesignation', sa.String(length=32767), nullable=True),
    sa.Column('tyreDesignation', sa.String(length=32767), nullable=True),
    sa.Column('loadCapacityIndex', sa.String(length=32767), nullable=True),
    sa.Column('loadCapacityIndex2', sa.String(length=32767), nullable=True),
    sa.Column('loadCapacityIndex3', sa.String(length=32767), nullable=True),
    sa.Column('loadCapacityIndex4', sa.String(length=32767), nullable=True),
    sa.Column('speedCategorySymbol', sa.String(length=32767), nullable=True),
    sa.Column('speedCategorySymbol2', sa.String(length=32767), nullable=True),
    sa.Column('loadCapacityIndicator', sa.String(length=32767), nullable=True),
    sa.Column('tyreClass', sa.String(length=32767), nullable=True),
    sa.Column('energyClass', sa.String(length=32767), nullable=True),
    sa.Column('wetGripClass', sa.String(length=32767), nullable=True),
    sa.Column('externalRollingNoiseValue', sa.String(length=32767), nullable=True),
    sa.Column('externalRollingNoiseClass', sa.String(length=32767), nullable=True),
    sa.Column('severeSnowTyre', sa.String(length=32767), nullable=True),
    sa.Column('iceTyre', sa.String(length=32767), nullable=True),
    sa.Column('eprel_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['eprel_id'], ['common.eprel_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('washerdriers2019',
    sa.Column('energyClassWashAndDry', sa.String(length=32767), nullable=True),
    sa.Column('energyClassWash', sa.String(length=32767), nullable=True),
    sa.Column('energyConsumption100WashAndDry', sa.String(length=32767), nullable=True),
    sa.Column('energyConsumption100Wash', sa.String(length=32767), nullable=True),
    sa.Column('ratedCapacityWashAndDry', sa.String(length=32767), nullable=True),
    sa.Column('ratedCapacityWash', sa.String(length=32767), nullable=True),
    sa.Column('waterConsumptionWashAndDry', sa.String(length=32767), nullable=True),
    sa.Column('waterConsumptionWash', sa.String(length=32767), nullable=True),
    sa.Column('programDurationRatedWashAndDry', sa.String(length=32767), nullable=True),
    sa.Column('programDurationRatedWash', sa.String(length=32767), nullable=True),
    sa.Column('spinClass', sa.String(length=32767), nullable=True),
    sa.Column('noise', sa.String(length=32767), nullable=True),
    sa.Column('noiseClass', sa.String(length=32767), nullable=True),
    sa.Column('eprel_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['eprel_id'], ['common.eprel_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('washingmachines2019',
    sa.Column('energyClass', sa.String(length=32767), nullable=True),
    sa.Column('energyConsPerCycle', sa.String(length=32767), nullable=True),
    sa.Column('energyConsPer100Cycle', sa.String(length=32767), nullable=True),
    sa.Column('ratedCapacity', sa.String(length=32767), nullable=True),
    sa.Column('programmeDurationRated', sa.String(length=32767), nullable=True),
    sa.Column('waterCons', sa.String(length=32767), nullable=True),
    sa.Column('spinClass', sa.String(length=32767), nullable=True),
    sa.Column('noise', sa.String(length=32767), nullable=True),
    sa.Column('noiseClass', sa.String(length=32767), nullable=True),
    sa.Column('eprel_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['eprel_id'], ['common.eprel_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('washingmachines2019')
    op.drop_table('washerdriers2019')
    op.drop_table('tyres')
    op.drop_table('refrigeratingappliances2019')
    op.drop_table('lightsources')
    op.drop_table('electronicdisplays')
    op.drop_table('dishwashers2019')
    op.drop_table('common')
    # ### end Alembic commands ###