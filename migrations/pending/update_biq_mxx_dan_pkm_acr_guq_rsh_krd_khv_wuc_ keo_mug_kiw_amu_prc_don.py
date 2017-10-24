# coding=ascii
"""update biq mxx dan pkm acr guq rsh krd khv wuc keo mug kiw amu prc don

Revision ID: 
Revises: 
Create Date: 

"""
from __future__ import unicode_literals

# revision identifiers, used by Alembic.
revision = ''
down_revision = ''

import string
import datetime

from alembic import op
import sqlalchemy as sa

ID_BEFORE_AFTER = {
    'biq': {  # https://github.com/clld/wals-data/issues/112
        'name': ('Bilaan', 'Bilaan (Koronadal)'),
        'iso': (['bps', 'smk'], 'bpr'),
        # FIXME: drop bps smk intended?
    },
    'mxx': {  # https://github.com/clld/wals-data/issues/100
        'macroarea': (None, 'North America'),
        'iso': ([], 'mxp'),
    },
    'dan': {  # https://github.com/clld/wals-data/issues/97
        'iso': (['daf'], 'dnj'),
    },
    'pkm': {  # https://github.com/clld/wals-data/issues/88 also in reassign_iso_codes_glottocodes_and_el.py
        'iso': (['pob', 'poh'], 'poh'),
        # FIXME: drop pob intended?
    },
    'aci': {  # https://github.com/clld/wals-data/issues/86 also in reassign_iso_codes_glottocodes_and_el.py
        'iso': (['acc', 'acr'], 'acr'),
    },
    'guq': {  # https://github.com/clld/wals-data/issues/80
        'iso': ([], 'cbd'),
    },
    # https://github.com/clld/wals-data/issues/75
    'rsh': {
        'name': ('Rushan', 'Shughni'),
    },
    'krd': {
        'iso': (['kmr'], 'ckb'),
        # FIXME: also nort2641 -> cent1972?
    },
    'khv': {
        'name': ('Khvarshi', ' Khwarshi'),
    },
    'wuc': {
        'name': ('Wu (Changzhou)', 'Wu'),
    },
    'keo': {
        'name': ("Ke'o", 'Keo'),
    },
    'mug': {
        'name': ('Mugil', 'Bargam'),
    },
    'kiw': {
        'name': ('Kiwai', ' Kiwai (Southern)'),
        'iso': (['kiw', 'kjd'], 'kjd'),
        # FIXME: also none -> sout2949?
    },
    'amu': {
        'name': ("Yanesha'", 'Amuesha'),
    },
    'prc': {
        'name': ('Parecis', 'Paresi'),
        'latlon': ((-14.0, -57.0), (-14.0, -57.5)),
    },
    'don': {  # https://github.com/clld/wals-data/issues/71
        'name': ('Dong', 'Dong (Southern)'),
        'iso': (['doc', 'kmc'], 'kmc'),
        # FIXME: also none -> sout2741?
    },
}


def ascii_name(s, _whitelist=set(string.ascii_lowercase + ' ()0123456789')):
    assert all(ord(c) < 128 for c in s)
    return ''.join(c for c in s.lower() if c in _whitelist)


def upgrade():
    conn = op.get_bind()

    l = sa.table('language', *map(sa.column, ['pk', 'updated', 'id', 'name', 'latitude', 'longitude']))
    w = sa.table('walslanguage', *map(sa.column, ['pk', 'ascii_name', 'macroarea']))
    icols = ['created', 'updated', 'active', 'version', 'id', 'type', 'description', 'lang', 'name']
    i = sa.table('identifier', *map(sa.column, ['pk'] + icols))
    licols = ['created', 'updated', 'active', 'version', 'language_pk', 'identifier_pk']
    li = sa.table('languageidentifier', *map(sa.column, licols))

    lwhere = (l.c.id == sa.bindparam('id_'))

    update_lang = l.update(bind=conn).where(lwhere)\
        .where(l.c.name == sa.bindparam('before'))\
        .values(updated=sa.func.now(), name=sa.bindparam('after'))

    wwhere = sa.exists().where(w.c.pk == l.c.pk).where(lwhere)

    update_wals = w.update(bind=conn).where(wwhere)\
        .where(w.c.ascii_name == sa.bindparam('ascii_before'))\
        .values(ascii_name=sa.bindparam('ascii_name'))

    iotherwhere = sa.and_(
        i.c.type == sa.bindparam('type', 'name'),
        i.c.description == sa.bindparam('description', 'other'),
        i.c.name == sa.bindparam('after'))

    delete_li = li.delete(bind=conn)\
        .where(sa.exists()
            .where(li.c.language_pk == l.c.pk).where(lwhere)
            .where(li.c.identifier_pk == i.c.pk).where(iotherwhere))

    delete_i = i.delete(bind=conn).where(iotherwhere)\
        .where(~sa.exists().where(li.c.identifier_pk == i.c.pk))

    update_latlon = l.update(bind=conn).where(lwhere)\
        .where(l.c.latitude == sa.bindparam('lat_before'))\
        .where(l.c.longitude == sa.bindparam('lon_before'))\
        .values(updated=sa.func.now(),
            latitude=sa.bindparam('lat_after'), longitude=sa.bindparam('lon_after'))

    add_lang_ma = l.update(bind=conn).where(lwhere)\
        .where(sa.exists().where(l.c.pk == w.c.pk)
            .where(w.c.macroarea == None))\
        .values(updated=sa.func.now())

    add_wals_ma = w.update(bind=conn).where(wwhere)\
        .where(w.c.macroarea == None)\
        .values(macroarea=sa.bindparam('after'))

    itype, ilang = (sa.bindparam(*a) for a in [('type', 'iso639-3'), ('lang', 'en')])
    iwhere = (i.c.type == itype)

    liwhere = sa.exists()\
        .where(li.c.language_pk == l.c.pk).where(lwhere)\
        .where(li.c.identifier_pk == i.c.pk).where(iwhere)

    before, after = map(sa.bindparam, ['before', 'after'])

    unlink_iso = li.delete(bind=conn)\
        .where(liwhere.where(i.c.name.op('IN')(before)).where(i.c.name != after))

    iid, idesc = (sa.bindparam('after') for _ in range(2))

    insert_iso = i.insert(bind=conn).from_select(icols,
        sa.select([sa.func.now(), sa.func.now(), True, 1, iid, itype, idesc, ilang, after])
        .where(~sa.exists().where(iwhere).where(i.c.name == after)))

    l_pk = sa.select([l.c.pk]).where(lwhere).as_scalar()
    i_pk = sa.select([i.c.pk]).where(iwhere).where(i.c.name == after).as_scalar()

    link_iso = li.insert(bind=conn).from_select(licols,
        sa.select([sa.func.now(), sa.func.now(), True, 1, l_pk, i_pk])
        .where(~liwhere.where(i.c.name == after)))

    for id_, fields in sorted(ID_BEFORE_AFTER.items()):
        if 'name' in fields:
            before, after = fields['name']
            update_lang.execute(id_=id_, before=before, after=after)
            update_wals.execute(id_=id_, ascii_before=ascii_name(before), ascii_name=ascii_name(after))
            delete_li.execute(id_=id_, after=after)
            delete_i.execute(id_=id_, after=after)
        if 'latlon' in fields:
            (lat_before, lon_before), (lat_after, lon_after) = fields['latlon']
            update_latlon.execute(id_=id_, lat_before=lat_before, lon_before=lon_before,
                                  lat_after=lat_after, lon_after=lon_after)
        if 'macroarea' in fields:
            before, after = fields['macroarea']
            assert before is None
            add_lang_ma.execute(id_=id_)
            add_wals_ma.execute(id_=id_, after=after).rowcount
        if 'iso' in fields:
            before, after = fields['iso']
            if before:
                unlink_iso.execute(id_=id_, before=tuple(before), after=after)
            insert_iso.execute(after=after)
            link_iso.execute(id_=id_, after=after)
 
    raise NotImplementedError


def downgrade():
    pass
