# coding=utf-8
"""issues 40-50

Revision ID: 3c1123e890e8
Revises: 36897f06d33c
Create Date: 2015-10-12 13:05:54.192640

"""
from __future__ import unicode_literals
import datetime

from alembic import op
import sqlalchemy as sa

from clld.util import slug
from clld.db.models.common import Config, Language

from wals3.migration import Connection
from wals3.models import Genus, Family, WalsLanguage

# revision identifiers, used by Alembic.
revision = '3c1123e890e8'
down_revision = u'36897f06d33c'


def upgrade():
    conn = Connection(op.get_bind())

    # https://github.com/clld/wals-data/issues/50
    fpk = conn.pk(Family, 'utoaztecan')
    gname = 'California Uto-Aztecan'
    gid = slug(gname)
    gpk = conn.insert(Genus, id=gid, name=gname, icon='fffff00', family_pk=fpk)

    for oid in ['takic', 'tubatulabal']:
        opk = conn.pk(Genus, oid)
        conn.update(WalsLanguage, dict(genus_pk=gpk), genus_pk=opk)
        conn.insert(Config, key=Config.replacement_key(Genus, oid), value=gid)
        conn.delete(Genus, id=oid)

    # https://github.com/clld/wals-data/issues/49
    conn.update_name('aym', 'Aymara (Central)')
    conn.update_glottocode('aym', 'cent2142')
    conn.update_iso('aym', 'ayr', ayc='Southern Aymara')

    # https://github.com/clld/wals-data/issues/48
    # The genus Guaymi should be renamed Guaymiic.
    conn.update(Genus, dict(name='Guaymiic'), id='guaymi')

    # The genus Aruak should be renamed Arhuacic.
    conn.update(Genus, dict(name='Arhuacic'), id='aruak')

    # The language Motilón should be renamed Barí (while keeping Motilón as the name of
    # the genus).
    conn.update_name('mti', 'Barí')

    # The genus Chibchan Proper should be split into two genera, Chibcha-Duit, containing
    # the language Muisca, and Tunebo, containing the language Tunebo.
    conn.update_genus(
        'msc', ('chibchaduit', 'Chibcha-Duit', 'fffff00'), family='chibchan')
    conn.update_genus(
        'tnb', ('tunebo', 'Tunebo', 'fffcc00'), family='chibchan')
    conn.insert(
        Config, key=Config.replacement_key(Genus, 'chibchanproper'), value=Config.gone)
    conn.delete(Genus, id='chibchanproper')

    # https://github.com/clld/wals-data/issues/44
    conn.update_name('jlu', 'Luwo', other='Jur Luwo')

    # https://github.com/clld/wals-data/issues/43
    conn.update_genus('ctw', ('catawban', 'Catawban', 'fffcc00'), family='siouan')
    conn.update(Genus, dict(name='Core Siouan'), id='siouan')

    # https://github.com/clld/wals-data/issues/40
    conn.update_source('Sumbuk-2002', year='1999', name='Sumbuk 1999')


def downgrade():
    pass
