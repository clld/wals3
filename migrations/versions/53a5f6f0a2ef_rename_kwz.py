# coding=utf-8
"""rename kwz

Revision ID: 53a5f6f0a2ef
Revises: 48b2bfaf9938
Create Date: 2015-03-09 10:35:24.135000

"""

# revision identifiers, used by Alembic.
revision = '53a5f6f0a2ef'
down_revision = '48b2bfaf9938'

import datetime

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute(sa.text('UPDATE language SET updated = now(), '
        'name = :after WHERE id = :id AND name = :before'
        ).bindparams(id='kwz', before=u'Kwaz\xe1', after='Kwaza'))


def downgrade():
    pass
