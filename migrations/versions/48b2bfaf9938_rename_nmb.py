# coding=utf-8
"""rename nmb

Revision ID: 48b2bfaf9938
Revises: 52167a1500ca
Create Date: 2015-03-09 10:10:49.268000

"""

# revision identifiers, used by Alembic.
revision = '48b2bfaf9938'
down_revision = '52167a1500ca'

import datetime

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute(sa.text('UPDATE language SET updated = now(), '
        'name = :after WHERE id = :id AND name = :before'
        ).bindparams(id='nmb',
        before=u'Nambiku\xe1ra', after=u'Nambiku\xe1ra (Southern)'))
    op.execute(sa.text('UPDATE language SET updated = now(), '
        'latitude = :lat_after, longitude = :lon_after '
        'WHERE id = :id AND latitude = :lat_before AND longitude = :lon_before'
        ).bindparams(id='nmb',
        lat_before=-13, lat_after=-14,
        lon_before=-59, lon_after=-59.5))
    

def downgrade():
    pass
