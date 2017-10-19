# coding=ascii
"""remove identical altnames

Revision ID: 2b25a82cb061
Revises: 3be1ca59b931
Create Date: 2017-10-19 15:00:18.871000

"""
from __future__ import unicode_literals

# revision identifiers, used by Alembic.
revision = '2b25a82cb061'
down_revision = u'3be1ca59b931'

import datetime

from alembic import op
import sqlalchemy as sa


def upgrade():
    l = sa.table('language', *map(sa.column, ['pk', 'id', 'name']))
    li = sa.table('languageidentifier', *map(sa.column, ['pk', 'language_pk', 'identifier_pk']))
    i = sa.table('identifier', *map(sa.column, ['pk', 'type', 'description', 'lang', 'name']))

    drop = sa.select([li.c.pk.label('li_pk'), i.c.pk.label('i_pk')])\
        .select_from(l
            .join(li, li.c.language_pk == l.c.pk)
            .join(i, sa.and_(
                li.c.identifier_pk == i.c.pk,
                i.c.type == 'name',
                i.c.description == 'other',
                i.c.lang == 'en')))\
        .where(l.c.name == i.c.name)\
        .order_by(l.c.id)

    # http://docs.sqlalchemy.org/en/latest/changelog/migration_11.html#cte-support-for-insert-update-delete
    # sa.delete(li).where(li.c.pk.in_(sa.select([drop.cte().c.li_pk])))
    # sa.delete(i).where(i.c.pk.in_(sa.select([drop.cte().c.i_pk])))

    conn = op.get_bind()
    for li_pk, i_pk in conn.execute(drop):
        conn.execute(sa.delete(li).where(li.c.pk == li_pk))
        conn.execute(sa.delete(i).where(i.c.pk == i_pk))


def downgrade():
    pass
