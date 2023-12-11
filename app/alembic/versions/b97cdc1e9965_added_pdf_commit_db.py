"""Added PDF Commit DB

Revision ID: b97cdc1e9965
Revises: 577d3e96e82a
Create Date: 2023-12-11 10:11:31.593173

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'b97cdc1e9965'
down_revision: Union[str, None] = '577d3e96e82a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pdfcommit',
    sa.Column('pdf_commit_datetime', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pdfcommit')
    # ### end Alembic commands ###