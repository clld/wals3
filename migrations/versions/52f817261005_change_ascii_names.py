# coding=ascii
"""change ascii names

Revision ID: 52f817261005
Revises: 2b25a82cb061
Create Date: 2017-10-19 17:07:30.725000

"""
from __future__ import unicode_literals

# revision identifiers, used by Alembic.
revision = '52f817261005'
down_revision = u'2b25a82cb061'

import datetime
import string
import unicodedata

from alembic import op
import sqlalchemy as sa


def ascii_name(s, _whitelist=set(string.ascii_lowercase + ' ()0123456789')):
    """

    >>> print(ascii_name('Bobo Madar\xe9 (Northern)'))
    bobo madare (northern)

    >>> print(ascii_name('Chumash (Barbare\xf1o)'))
    chumash (barbareno)
    """
    s = ''.join(c for c in unicodedata.normalize('NFD', s)
                if not unicodedata.combining(c))
    return ''.join(c for c in s.lower() if c in _whitelist)


def upgrade(verbose=True):
    conn = op.get_bind()

    l = sa.table('language', *map(sa.column, ['pk', 'id', 'name']))
    w = sa.table('walslanguage', *map(sa.column, ['pk', 'ascii_name']))

    query = sa.select([l.c.id, l.c.name, w.c.ascii_name], bind=conn)\
        .select_from(l.join(w, l.c.pk == w.c.pk))\
        .order_by(l.c.id)

    update = sa.update(w, bind=conn)\
        .where(sa.exists().where(sa.and_(
            l.c.pk == w.c.pk,
            l.c.id == sa.bindparam('id_'))))\
        .where(w.c.ascii_name == sa.bindparam('before'))\
        .values(ascii_name=sa.bindparam('after'))

    for id_, name, before in query.execute():
        after = ascii_name(name)
        if after != before:
            if verbose:
                print('%s %s: %s -> %s' % (id_, name, before, after))
            update.execute(id_=id_, before=before, after=after)


def downgrade():
    pass
