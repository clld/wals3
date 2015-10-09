# coding=utf-8
"""fix glottocodes

Revision ID: 13b08c8d306b
Revises: 42f4c3147ade
Create Date: 2015-10-09 10:54:19.096927

"""
from __future__ import unicode_literals

# revision identifiers, used by Alembic.
revision = '13b08c8d306b'
down_revision = u'42f4c3147ade'

import datetime

from alembic import op
import sqlalchemy as sa

from clld.db.models import common
from wals3.migration import Connection


def upgrade():
    conn = Connection(op.get_bind())

    # https://github.com/clld/wals-data/issues/58
    conn.update_glottocode('uhi', 'atam1239')

    # https://github.com/clld/wals-data/issues/57
    conn.update_glottocode('mdm', 'west2443')
    conn.update_glottocode('wem', 'west2443')

    # https://github.com/clld/wals-data/issues/56
    conn.update_glottocode('wdo', 'pitj1243')

    # https://github.com/clld/wals-data/issues/55
    conn.update_glottocode('wir', 'wira1265')

    # https://github.com/clld/wals-data/issues/51
    lpk = conn.pk(common.Language, 'gno')
    ipk = conn.insert(common.Identifier, name='Kotiria', description='other', type='name')
    conn.insert(common.LanguageIdentifier, identifier_pk=ipk, language_pk=lpk)


def downgrade():
    pass
