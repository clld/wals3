# coding=ascii
"""change country from SD to SS

Revision ID: 15da24f7a5af
Revises: 39c1fbfc53ce
Create Date: 2017-11-08 15:37:26.926000

"""
from __future__ import unicode_literals

# revision identifiers, used by Alembic.
revision = '15da24f7a5af'
down_revision = u'39c1fbfc53ce'

import datetime

from alembic import op
import sqlalchemy as sa

# https://github.com/clld/wals-data/issues/99
IDS = [  # 27
    'acl',
    'aja',
    'any',
    'avo',
    'bar',
    'bgo',
    'big',
    'bka',
    'blj',
    'cai',
    'did',
    'din',
    'jlu',
    'jmo',
    'kom',
    'kre',
    'kuk',
    'mdu',
    'mou',
    'mrl',
    'ndg',
    'nue',
    'par',
    'shl',
    'ten',
    'yul',
    'zan',
]

UNCHANGED_SD = [  # 32
    'ams', 'bej', 'ber', 'ddf', 'fur', 'gmz', 'igs', 'jom', 'kad', 'knr',
    'kro', 'ktc', 'ktl', 'laf', 'mad', 'mid', 'mii', 'mro', 'msk', 'msl',
    'nbd', 'nbh', 'nob', 'nyi', 'ori', 'otr', 'ras', 'sht', 'tia', 'tma',
    'tmn', 'zag',
]

BEFORE, AFTER, NAME, CONTINENT = 'SD', 'SS', 'South Sudan', 'Africa'


def upgrade():
    conn = op.get_bind()

    l = sa.table('language', *map(sa.column, ['pk', 'id', 'name']))
    ccols = ['created', 'updated', 'active', 'id', 'name', 'continent']
    c = sa.table('country', *map(sa.column, ['pk'] + ccols))
    lccols = ['created', 'updated', 'active', 'language_pk', 'country_pk']
    lc = sa.table('countrylanguage', *map(sa.column, lccols))

    lwhere = (l.c.id == sa.bindparam('id_'))

    cid, cname, ccont = map(sa.bindparam, ['cc', 'name', 'continent'])
    cwhere = (c.c.id == cid)

    insert_c = c.insert(bind=conn).from_select(ccols,
        sa.select([sa.func.now(), sa.func.now(), True, cid, cname, ccont])
        .where(~sa.exists().where(cwhere)))

    liwhere = sa.exists()\
        .where(lc.c.language_pk == l.c.pk).where(lwhere)\
        .where(lc.c.country_pk == c.c.pk).where(cwhere)

    unlink_country = lc.delete(bind=conn).where(liwhere)

    l_pk = sa.select([l.c.pk]).where(lwhere).as_scalar()
    c_pk = sa.select([c.c.pk]).where(cwhere).as_scalar()

    link_country = lc.insert(bind=conn).from_select(lccols,
        sa.select([sa.func.now(), sa.func.now(), True, l_pk, c_pk])
        .where(~liwhere))

    insert_c.execute(cc=AFTER, name=NAME, continent=CONTINENT)
    for id_ in IDS:
        unlink_country.execute(id_=id_, cc=BEFORE)
        link_country.execute(id_=id_, cc=AFTER)


def downgrade():
    pass
