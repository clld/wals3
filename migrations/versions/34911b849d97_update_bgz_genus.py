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

    lwhere = (l.c.id == sa.bindparam('id_'))

    gbefore, gafter = (g.c.id == sa.bindparam(n) for n in ['before', 'after'])

    wwhere = sa.and_(
        sa.exists()
            .where(w.c.pk == l.c.pk).where(lwhere)
            .where(w.c.genus_pk == g.c.pk).where(gbefore),
        sa.exists().where(gafter))

    update_lang = l.update(bind=conn).where(lwhere)\
        .where(wwhere)\
        .values(updated=sa.func.now())

    update_wals = w.update(bind=conn).where(wwhere)\
        .values(genus_pk=g.select().with_only_columns([g.c.pk]).where(gafter))

    update_lang.execute(id_=ID, before=BEFORE, after=AFTER)
    update_wals.execute(id_=ID, before=BEFORE, after=AFTER)
    

def downgrade():
    pass
