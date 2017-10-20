# coding=utf-8
"""update bgz genus

Revision ID: 34911b849d97
Revises: 430f8e3d07bf
Create Date: 2017-10-20 14:52:13.953000

"""
from __future__ import unicode_literals

# revision identifiers, used by Alembic.
revision = '34911b849d97'
down_revision = u'430f8e3d07bf'

import datetime

from alembic import op
import sqlalchemy as sa

# https://github.com/clld/wals-data/issues/113
ID, BEFORE, AFTER = 'bgz', 'barito', 'northborneo'


def upgrade():
    conn = op.get_bind()

    l = sa.table('language', *map(sa.column, ['pk', 'id', 'updated']))
    w = sa.table('walslanguage', *map(sa.column, ['pk', 'genus_pk']))
    g = sa.table('genus', *map(sa.column, ['pk', 'id']))

    g_before = sa.select([g.c.pk]).where(g.c.id == sa.bindparam('before'))
    update_lang = sa.update(l, bind=conn)\
        .where(l.c.id == sa.bindparam('id_'))\
        .where(sa.exists().where(sa.and_(
            w.c.pk == l.c.pk,
            w.c.genus_pk == g_before)))\
        .values(updated=sa.func.now())

    g_after = sa.select([g.c.pk]).where(g.c.id == sa.bindparam('after'))
    update_wals = sa.update(w, bind=conn)\
        .where(sa.exists().where(sa.and_(
            l.c.pk == w.c.pk,
            l.c.id == sa.bindparam('id_'))))\
        .where(sa.exists().where(sa.and_(
            g.c.pk == w.c.genus_pk,
            g.c.id == sa.bindparam('before'))))\
        .values(genus_pk=g_after)

    update_lang.execute(id_=ID, before=BEFORE)
    update_wals.execute(id_=ID, before=BEFORE, after=AFTER)
    

def downgrade():
    pass
