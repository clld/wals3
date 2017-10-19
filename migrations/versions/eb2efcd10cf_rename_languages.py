# coding=ascii
"""rename languages

Revision ID: eb2efcd10cf
Revises: 183a783fc885
Create Date: 2017-10-18 17:35:41.835000

"""
from __future__ import unicode_literals

# revision identifiers, used by Alembic.
revision = 'eb2efcd10cf'
down_revision = u'183a783fc885'

import string
import datetime

from alembic import op
import sqlalchemy as sa


ID_BEFORE_AFTER_KEEP = {
    # https://github.com/clld/wals-data/issues/123
    'bng': ('Baining', 'Qaget', False),
    # https://github.com/clld/wals-data/issues/109
    'kag': ('Kayu Agung', 'Komering', True),
    # https://github.com/clld/wals-data/issues/108
    'abb': ('Arabic (Abb\xe9ch\xe9 Chad)', 'Arabic (Chadian)', False),
    # https://github.com/clld/wals-data/issues/102
    'tec': ('Teco', 'Tectiteco', False),
    # https://github.com/clld/wals-data/issues/101
    'say': ('Sayultec', 'Sayula Popoluca', False),
    # https://github.com/clld/wals-data/issues/98
    'bka': ('Baka (in Sudan)', 'Baka (in South Sudan)', False),
    # https://github.com/clld/wals-data/issues/94
    'ygd': ('Yag Dii', 'Dii', False),
    # https://github.com/clld/wals-data/issues/93
    'pcm': ('Pocomam', 'Poqomam', False),
    # https://github.com/clld/wals-data/issues/91
    'bpb': ('Bahnar (Plei Bong-Mang Yang)', 'Bahnar', False),
    # https://github.com/clld/wals-data/issues/84
    'chu': ('Chulup\xed', 'Nivacle', False),
    # https://github.com/clld/wals-data/issues/73
    'zqs': ('Zoque (Soteapan)', 'Popoluca (Sierra)', False),
    # https://github.com/clld/wals-data/issues/68
    'mug': ('Mugil', 'Bargam', False),
}


def ascii_name(name):
    assert all(ord(c) < 128 for c in name)
    return ''.join(c for c in name.lower() if c in string.ascii_lowercase)


def upgrade():
    conn = op.get_bind()

    language = sa.table('language', *map(sa.column, ['pk', 'id', 'name', 'updated']))
    lid = sa.bindparam('id_')
    lbefore = sa.bindparam('before')
    update_lang = sa.update(language, bind=conn)\
        .where(sa.and_(
            language.c.id == lid,
            language.c.name == lbefore))\
        .values(updated=sa.func.now(), name=sa.bindparam('after'))

    walslanguage = sa.table('walslanguage', *map(sa.column, ['pk', 'ascii_name']))
    aname = sa.bindparam('ascii_name')
    update_wals = sa.update(walslanguage, bind=conn)\
        .where(sa.exists().where(sa.and_(
            language.c.pk == walslanguage.c.pk,
            language.c.id == lid))\
        .where(walslanguage.c.ascii_name != aname))\
        .values(ascii_name=aname)

    icols = ['created', 'updated', 'active', 'version', 'type', 'description', 'lang', 'name']
    identifier = sa.table('identifier', *map(sa.column, ['pk'] + icols))
    itype, idesc, ilang = (sa.bindparam(*a) for a in [('type', 'name'), ('description', 'other'), ('lang', 'en')])
    iname = sa.bindparam('name')
    iwhere = sa.and_(
        identifier.c.type == itype,
        identifier.c.description == idesc,
        identifier.c.lang == ilang,
        identifier.c.name == iname)
    insert_ident = sa.insert(identifier, bind=conn).from_select(icols,
        sa.select([sa.func.now(), sa.func.now(), True, 1, itype, idesc, ilang, iname])
        .where(~sa.exists().where(iwhere)))

    licols = ['created', 'updated', 'active', 'version', 'language_pk', 'identifier_pk']
    languageidentifier = sa.table('languageidentifier', *map(sa.column, licols))
    l_pk = sa.select([language.c.pk]).where(language.c.id == lid)
    i_pk = sa.select([identifier.c.pk]).where(sa.and_(iwhere))
    insert_lang_ident = sa.insert(languageidentifier, bind=conn).from_select(licols,
        sa.select([sa.func.now(), sa.func.now(), True, 1, l_pk.as_scalar(), i_pk.as_scalar()])
        .where(~sa.exists().where(sa.and_(
            languageidentifier.c.language_pk == l_pk,
            languageidentifier.c.identifier_pk == i_pk))))

    for id_, (before, after, keep) in sorted(ID_BEFORE_AFTER_KEEP.items()):
        update_lang.execute(id_=id_, before=before, after=after)
        update_wals.execute(id_=id_, ascii_name=ascii_name(after))
        if keep:
            insert_ident.execute(name=before)
            insert_lang_ident.execute(id_=id_, name=before)


def downgrade():
    pass
