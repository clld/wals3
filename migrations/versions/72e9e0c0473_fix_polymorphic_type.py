# coding=utf-8
"""fix polymorphic_type

Revision ID: 72e9e0c0473
Revises: 547d1f4ea331
Create Date: 2014-11-26 16:06:38.549000

"""

# revision identifiers, used by Alembic.
revision = '72e9e0c0473'
down_revision = '547d1f4ea331'

import datetime

from alembic import op
import sqlalchemy as sa


def upgrade():
    update_pmtype(['language', 'language_history', 'contribution', 'contribution_history',
        'parameter', 'parameter_history'], 'base', 'custom')


def downgrade():
    update_pmtype(['language', 'language_history', 'contribution', 'contribution_history',
        'parameter', 'parameter_history'], 'custom', 'base')


def update_pmtype(tablenames, before, after):
    for table in tablenames:
        op.execute(sa.text('UPDATE %s SET polymorphic_type = :after '
            'WHERE polymorphic_type = :before' % table
            ).bindparams(before=before, after=after))
