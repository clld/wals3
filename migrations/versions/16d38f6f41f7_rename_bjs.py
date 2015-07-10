# coding=utf-8
"""rename bjs

Revision ID: 16d38f6f41f7
Revises: 24135382644f
Create Date: 2015-07-10 09:48:57.427063

"""
from __future__ import unicode_literals

# revision identifiers, used by Alembic.
revision = '16d38f6f41f7'
down_revision = '24135382644f'

from alembic import op

from clld.db.migration import Connection
from clld.db.models.common import Language

from wals3.models import WalsLanguage


def upgrade():
    """Bajau (Semporna) should be renamed Sama (Southern)."""
    conn = Connection(op.get_bind())

    bjs = conn.pk(Language, 'bjs')
    conn.update(Language, dict(name='Sama (Southern)'), pk=bjs)
    conn.update(WalsLanguage, dict(ascii_name='samasouthern'), pk=bjs)


def downgrade():
    pass
