# coding=utf-8
"""WALS 2013

Revision ID: 274ff6197e85
Revises: None
Create Date: 2013-10-30 21:43:35.339017

"""

# revision identifiers, used by Alembic.
revision = '274ff6197e85'
down_revision = None

import datetime

from alembic import op
import sqlalchemy as sa


def upgrade():
    conn = op.get_bind()
    #12
    conn.execute("update identifier set name = 'Bembe' where name = 'Bembe (CK if same Bembe)'")


def downgrade():
    pass
