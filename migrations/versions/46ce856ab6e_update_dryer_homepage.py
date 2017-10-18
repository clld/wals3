# coding=utf-8
"""update dryer homepage

Revision ID: 46ce856ab6e
Revises: 3c1123e890e8
Create Date: 2017-10-18 14:04:01.491000

"""
from __future__ import unicode_literals

# revision identifiers, used by Alembic.
revision = '46ce856ab6e'
down_revision = u'3c1123e890e8'

import datetime

from alembic import op
import sqlalchemy as sa

ID = 'dryerms'

BEFORE = 'http://linguistics.buffalo.edu/people/faculty/dryer/dryer/dryer.htm'
AFTER = 'http://www.acsu.buffalo.edu/~dryer/'


def upgrade():
    update_url = sa.text('UPDATE contributor SET updated = now(), url = :after '
                         'WHERE id = :id AND url = :before')
    op.execute(update_url.bindparams(id=ID, before=BEFORE, after=AFTER))


def downgrade():
    pass
