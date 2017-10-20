# coding=utf-8
"""add kua iso and el_name

Revision ID: 401b9b4b1045
Revises: 34911b849d97
Create Date: 2017-10-20 15:30:00.770000

"""
from __future__ import unicode_literals

# revision identifiers, used by Alembic.
revision = '401b9b4b1045'
down_revision = u'34911b849d97'

import datetime

from alembic import op
import sqlalchemy as sa

# https://github.com/clld/wals-data/issues/110

ID = 'kua'

ISO = 'sdm'

EL_ID = 'ethnologue-sdm'
EL_NAME = 'Semandang (dialect)'


def upgrade():
    conn = op.get_bind()
    
    l = sa.table('language', *map(sa.column, ['pk', 'id']))
    icols = ['created', 'updated', 'active', 'version', 'id', 'type', 'description', 'lang', 'name']
    i = sa.table('identifier', *map(sa.column, ['pk'] + icols))
    licols = ['created', 'updated', 'active', 'version', 'language_pk', 'identifier_pk']
    li = sa.table('languageidentifier', *map(sa.column, licols))

    l_pk = sa.select([l.c.pk]).where(l.c.id == sa.bindparam('id_')).as_scalar()
    i_pk = sa.select([i.c.pk]).where(sa.and_(i.c.type == 'iso639-3', i.c.name == sa.bindparam('iso'))).as_scalar()

    link_iso = sa.insert(li, bind=conn).from_select(licols,
        sa.select([sa.func.now(), sa.func.now(), True, 1, l_pk, i_pk])
        .where(~sa.exists().where(sa.and_(li.c.language_pk == l_pk, li.c.identifier_pk == i_pk))))

    itype, idesc, ilang = (sa.bindparam(*a) for a in [('type', 'name'), ('description', 'ethnologue'), ('lang', 'en')])
    iid, iname = map(sa.bindparam, ['id_', 'name'])

    iwhere = sa.and_(i.c.type == itype, i.c.description == idesc, i.c.name == iname)

    insert_ident = sa.insert(i, bind=conn).from_select(icols,
        sa.select([sa.func.now(), sa.func.now(), True, 1, iid, itype, idesc, ilang, iname])
        .where(~sa.exists().where(iwhere)))

    i_pk = sa.select([i.c.pk]).where(iwhere).as_scalar()

    insert_lang_ident = sa.insert(li, bind=conn).from_select(licols,
        sa.select([sa.func.now(), sa.func.now(), True, 1, l_pk, i_pk])
        .where(~sa.exists().where(sa.and_(li.c.language_pk == l_pk, li.c.identifier_pk == i_pk))))
    
    link_iso.execute(id_=ID, iso=ISO)
    insert_ident.execute(id_=EL_ID, name=EL_NAME)
    insert_lang_ident.execute(id_=ID, name=EL_NAME)
   

def downgrade():
    pass
