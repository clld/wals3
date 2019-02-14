# coding=utf-8
"""remove tabs in code names and descriptions

Revision ID: 126d014db657
Revises: 6d0d0b5416c5
Create Date: 2019-02-14 10:56:05.824161

"""
from __future__ import unicode_literals

# revision identifiers, used by Alembic.
revision = '126d014db657'
down_revision = '6d0d0b5416c5'

import datetime

from alembic import op
import sqlalchemy as sa


def upgrade():
    conn = op.get_bind()
    change = []
    for pk, name, description in conn.execute('select pk, name, description from domainelement'):
        if ('\t' in name) or ('\t' in description):
            change.append((pk, name.replace('\t', '  '), description.replace('\t', '  ')))
    for pk, name, description in change:
        conn.execute(
            'update domainelement set name = %s, description = %s where pk = %s',
            (name, description, pk))
    for pk, name, description in conn.execute('select pk, name, description from domainelement'):
        if ('\t' in name) or ('\t' in description):
            raise ValueError(pk)

def downgrade():
    pass
