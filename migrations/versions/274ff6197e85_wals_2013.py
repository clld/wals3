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

from clld.db.migration import update
from clld.db.models.common import Identifier


def upgrade():
    conn = op.get_bind()
    #12
    update(conn, Identifier, dict(name='Bembe'), name='Bembe (CK if same Bembe)')


def downgrade():
    pass
