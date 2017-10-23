# coding=utf-8
"""update biq mxx dan

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
    },
    'mxx': {  # https://github.com/clld/wals-data/issues/100
        'macroarea': (None, 'North America'),
        'iso': ([], 'mxp'),
    },
    'dan': {  # https://github.com/clld/wals-data/issues/97
        'iso': (['daf'], 'dnj'),
    },
}


def ascii_name(s, _whitelist=set(string.ascii_lowercase + ' ()0123456789')):
    assert all(ord(c) < 128 for c in s)
    return ''.join(c for c in s.lower() if c in _whitelist)


def upgrade():
    conn = op.get_bind()

    l = sa.table('language', *map(sa.column, ['pk', 'updated', 'id', 'name']))
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
