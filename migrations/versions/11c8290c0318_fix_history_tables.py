# coding=utf-8
"""fix history tables

Revision ID: 11c8290c0318
Revises: 12dbc8689bb
Create Date: 2014-07-25 12:53:02.368225

"""

# revision identifiers, used by Alembic.
revision = '11c8290c0318'
down_revision = u'12dbc8689bb'

import datetime

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('walslanguage_history',
        sa.Column('macroarea', sa.Unicode())
    )


def downgrade():
    pass
