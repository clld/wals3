# coding=utf-8
"""overhaul african languages

Revision ID: 58559d4eea0d
Revises: 342705ff1484
Create Date: 2015-07-10 10:30:43.660103

"""
from __future__ import unicode_literals

# revision identifiers, used by Alembic.
revision = '58559d4eea0d'
down_revision = u'342705ff1484'

import datetime

from alembic import op
import sqlalchemy as sa

from clld.util import slug
from clld.db.migration import Connection
from clld.db.models.common import Config

from wals3.models import Family, Genus


def upgrade():
    conn = Connection(op.get_bind())

    # Khoisan needs to be replaced by four families:
    # Sandawe (no name change)
    # Kxa: two genera: =|Hoan, Ju-Kung (a name change from 'Northern Khoisan')
    # Tu (a name change from Southern Khoisan)
    # Khoe-Kwadi (a name change from Central Khoisan)
    genera = {
        'hoan': ('Kxa', None),
        'sandawe': ('Sandawe', None),
        'centralkhoisan': ('Khoe-Kwadi', 'Khoe-Kwadi'),
        'southernkhoisan': ('Tu', 'Tu'),
        'northernkhoisan': ('Kxa', 'Ju-Kung'),
    }
    families = {}

    for gid, (fname, gname) in genera.items():
        fid = slug(fname)
        fpk = families.get(fid)
        if fpk is None:
            families[fid] = fpk = conn.insert(Family, id=fid, name=fname)
        values = dict(family_pk=fpk)
        if gname:
            values['name'] = gname
        conn.update(Genus, values, id=gid)

    conn.insert(Config, key=Config.replacement_key(Family, 'khoisan'), value=Config.gone)
    conn.delete(Family, id='khoisan')

    # Nilo-Saharan needs to be removed and replaced by the following families, with
    # constituent genera.
    # The following genera will now be families containing a single genus with the
    # same name:
    # Berta Kunama Songhay Gumuz Koman Shabo Kuliak Maban Fur
    for gname in 'Berta Kunama Songhay Gumuz Koman Shabo Kuliak Maban Fur'.split():
        gid = gname.lower()
        fpk = conn.insert(Family, id=gid, name=gname)
        gpk = conn.pk(Genus, gid)
        conn.update(Genus, dict(family_pk=fpk), pk=gpk)

    # The following is one family with two genera:
    # Saharan: Eastern Saharan, Western Saharan
    fpk = conn.insert(Family, id='saharan', name='Saharan')
    for gname in ['Eastern Saharan', 'Western Saharan']:
        conn.update(Genus, dict(family_pk=fpk), pk=conn.pk(Genus, gname, attr='name'))

    # What is currently the subfamily Central Sudanic becomes a family with the same name
    # and same constituent genera
    # and what is currently the subfamily Eastern Sudanic becomes a family with the same
    # name and the same constituent genera.
    for sfn in ['Central Sudanic', 'Eastern Sudanic']:
        fpk = conn.insert(Family, id=slug(sfn), name=sfn)
        conn.update(Genus, dict(family_pk=fpk, subfamily=None), subfamily=sfn)

    conn.insert(Config, key=Config.replacement_key(Family, 'nilosaharan'), value=Config.gone)
    conn.delete(Family, id='nilosaharan')

    # The following groups need to be removed from Niger-Congo and set up as separate
    # families. The last two (Dogon and Ijoid) are families containing one genus.
    # - Mande (currently a subfamily) with the following two genera:
    # Eastern Mande, Western Mande
    # - Kordofanian (currently a subfamily) with the following five genera:
    # Katla-Tima, Rashad, Heiban, Talodi (a name change from Talodi Proper),
    # and Lafofa (renamed from Tegem)
    # - Dogon
    # - Ijoid
    for sfn in ['Mande', 'Kordofanian']:
        fpk = conn.insert(Family, id=slug(sfn), name=sfn)
        conn.update(Genus, dict(family_pk=fpk, subfamily=None), subfamily=sfn)

    for old, new in {'Talodi Proper': 'Talodi', 'Tegem': 'Lafofa'}.items():
        conn.update(Genus, dict(name=new), name=old)

    for sfn in ['Dogon', 'Ijoid']:
        fpk = conn.insert(Family, id=slug(sfn), name=sfn)
        conn.update(Genus, dict(family_pk=fpk), name=sfn)

    # A minor change in the name of the family Kadugli to just Kadu.
    conn.update(Family, dict(name='Kadu'), name='Kadugli')


def downgrade():
    pass
