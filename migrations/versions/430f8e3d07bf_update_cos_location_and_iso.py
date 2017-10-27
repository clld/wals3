# coding=ascii
"""update cos location and iso

Revision ID: 430f8e3d07bf
Revises: 45055609733c
Create Date: 2017-10-20 13:58:01.089000

"""
from __future__ import unicode_literals

# revision identifiers, used by Alembic.
revision = '430f8e3d07bf'
down_revision = u'45055609733c'

import datetime

from alembic import op
import sqlalchemy as sa

# https://github.com/clld/wals-data/issues/129
ID = 'cos'

LAT_BEFORE, LON_BEFORE = (37.0, -122.0)

LAT_AFTER, LON_AFTER = (36.83333333333333333, -121.75)

ISO_BEFORE, ISO_AFTER = ('cst', 'css')


def upgrade():
    conn = op.get_bind()
    
    l = sa.table('language', *map(sa.column, ['pk', 'updated', 'id', 'latitude', 'longitude']))
    i = sa.table('identifier', *map(sa.column, ['pk', 'type', 'name']))
    licols = ['created', 'updated', 'active', 'version', 'language_pk', 'identifier_pk']
    li = sa.table('languageidentifier', *map(sa.column, licols))

    lwhere = (l.c.id == sa.bindparam('id_'))

    update_latlon = l.update(bind=conn).where(lwhere)\
        .where(l.c.latitude == sa.bindparam('lat_before'))\
        .where(l.c.longitude == sa.bindparam('lon_before'))\
        .values(updated=sa.func.now(),
                latitude=sa.bindparam('lat_after'), longitude=sa.bindparam('lon_after'))

    iwhere = sa.and_(i.c.type == 'iso639-3', i.c.name == sa.bindparam('iso'))

    liwhere = sa.exists()\
        .where(li.c.language_pk == l.c.pk).where(lwhere)\
        .where(li.c.identifier_pk == i.c.pk).where(iwhere)

    unlink_iso = li.delete(bind=conn).where(liwhere)

    l_pk = l.select().with_only_columns([l.c.pk]).where(lwhere).as_scalar()
    i_pk = i.select().with_only_columns([i.c.pk]).where(iwhere).as_scalar()

    link_iso = li.insert(bind=conn).from_select(licols,
        sa.select([sa.func.now(), sa.func.now(), True, 1, l_pk, i_pk])
        .where(~liwhere))

    update_latlon.execute(id_=ID,
                          lat_before=LAT_BEFORE, lon_before=LON_BEFORE,
                          lat_after=LAT_AFTER, lon_after=LON_AFTER)
    unlink_iso.execute(id_=ID, iso=ISO_BEFORE)
    link_iso.execute(id_=ID, iso=ISO_AFTER)


def downgrade():
    pass
