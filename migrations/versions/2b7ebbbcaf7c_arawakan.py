# coding=utf-8
"""arawakan

https://github.com/clld/wals-data/issues/61

Revision ID: 2b7ebbbcaf7c
Revises: 4e5cdd2c9cfe
Create Date: 2015-10-09 13:38:21.856426

"""
from __future__ import unicode_literals

# revision identifiers, used by Alembic.
revision = '2b7ebbbcaf7c'
down_revision = u'4e5cdd2c9cfe'

import datetime

from alembic import op
import sqlalchemy as sa

#from clld.util import slug
from clld.db.models.common import (
    Language, Source, LanguageSource, ValueSet, ValueSetReference, Config,
)
from clld.lib.bibtex import EntryType

from wals3.migration import Connection
from wals3.models import Family, Genus
from wals3.coordinates import Coordinates


def upgrade():
    conn = Connection(op.get_bind())

    # The genus for Yanesha’ needs to be renamed Yanesha’.
    conn.update(Genus, dict(name="Yanesha'"), id='westernarawakan')

    # Bahuana
    conn.update_name('bah', 'Xiriana')
    conn.update_glottocode('bah', 'xiri1243')
    conn.update_iso('bah', xir='Xiriâna')
    coords = Coordinates('2d40N', '62d30W')
    conn.update(
        Language, dict(latitude=coords.latitude, longitude=coords.longitude), id='bah')

    spk = conn.execute('select max(pk) from source').fetchone()[0] + 1
    lpk = conn.pk(Language, 'bah')
    spk = conn.insert(
        Source,
        pk=spk,
        id='Ramirez-1992',
        name='Ramirez 1992',
        description='Bahuana: une nouvelle langue de la famille Arawak',
        bibtex_type=EntryType.book,
        author='Ramirez, Henri',
        year='1992',
        title='Bahuana: une nouvelle langue de la famille Arawak',
        address='Paris',
        publisher='Amerindia')
    conn.insert(LanguageSource, language_pk=lpk, source_pk=spk)
    vspk = conn.pk(ValueSet, lpk, attr='language_pk')
    conn.insert(ValueSetReference, valueset_pk=vspk, source_pk=spk, description='35')

    # split northern arawakan
    GENERA = {
        'Alto-Orinoco': 'bnw mpr'.split(),
        'Caribbean Arawakan': 'ara grf goa'.split(),
        'Inland Northern Arawakan': 'acg bae cur ppc res tar wrk ycn'.split(),
        'Bahuanic': ['bah'],
        'Wapishanan': ['wps'],
    }
    ICONS = ['cdd0000', 'cffcc00', 'cffff00', 'cff6600', 'cffffcc']

    fpk = conn.pk(Family, 'arawakan')
    for icon, (name, lids) in zip(ICONS, GENERA.items()):
        gpk = conn.insert(Genus, id=slug(name), name=name, icon=icon, family_pk=fpk)
        for lid in lids:
            conn.update_genus(lid, gpk)

    conn.insert(
        Config,
        key=Config.replacement_key(Genus, 'northernarawakan'),
        value=Config.gone)
    conn.delete(Genus, id='northernarawakan')


def downgrade():
    pass
