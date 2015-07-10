# coding=utf-8
"""reclassify rji

Revision ID: 108c6a424057
Revises: 16d38f6f41f7
Create Date: 2015-07-10 10:01:57.525577

"""
from __future__ import unicode_literals

# revision identifiers, used by Alembic.
revision = '108c6a424057'
down_revision = u'16d38f6f41f7'

import datetime

from alembic import op
import sqlalchemy as sa

from clld.db.migration import Connection
from clld.db.models.common import Language

from wals3.models import Family, Genus, WalsLanguage


def upgrade():
    """
    Raji should be taken out
    of the Bodic genus and placed in a new genus Raji-Raute, but still part
    of the Tibeto-Burman subfamily of the Sino-Tibetan family.
    """
    conn = Connection(op.get_bind())
    pk = conn.pk(Family, 'sinotibetan')
    dizoid = conn.insert(
        Genus,
        id='rajiraute',
        name='Raji-Raute',
        family_pk=pk,
        subfamily='Tibeto-Burman',
        icon='tffff00')
    pk = conn.pk(Language, 'rji')
    conn.update(WalsLanguage, [('genus_pk', dizoid)], pk=pk)


def downgrade():
    pass
