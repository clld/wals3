# coding=utf-8
"""make dah dahalo

Revision ID: 245924ef4e97
Revises: 144fec4ed227
Create Date: 2014-12-09 16:28:39.875000

"""

# revision identifiers, used by Alembic.
revision = '245924ef4e97'
down_revision = '144fec4ed227'

import datetime

from alembic import op
import sqlalchemy as sa

GENUS = 'Dahalo'
ID = GENUS.lower()
FAMILY_ID = 'afroasiatic'
SUBFAMILY = 'Cushitic'
ICON = 'ccccccc'
LANGUAGE = 'dah'


def upgrade():
    conn = op.get_bind()

    exists_genus = sa.text('SELECT EXISTS (SELECT 1 FROM genus WHERE id = :id)',
        conn)

    select_family = sa.text('SELECT pk FROM family WHERE id = :id', conn)

    insert_genus = sa.text('INSERT INTO genus '
        '(created, updated, active, id, name, family_pk, subfamily, icon) VALUES '
        '(now(), now(), true, :id, :name, :family_pk, :subfamily, :icon)', conn)

    update_lang = sa.text('UPDATE language AS l SET updated = now() '
        'WHERE id = :id AND EXISTS (SELECT 1 FROM walslanguage WHERE pk = l.pk '
        'AND genus_pk != (SELECT pk FROM genus WHERE id = :genus_id))', conn)

    update_wals = sa.text('UPDATE walslanguage SET genus_pk = '
        '(SELECT pk FROM genus WHERE id = :genus_id) '
        'WHERE pk = (SELECT pk FROM language WHERE id = :id) '
        'AND genus_pk != (SELECT pk FROM genus WHERE id = :genus_id)', conn)

    if not exists_genus.scalar(id=ID):
        insert_genus.execute(id=ID, name=GENUS, icon=ICON,
            family_pk=select_family.scalar(id=FAMILY_ID),
            subfamily=SUBFAMILY)

    update_lang.execute(id=LANGUAGE, genus_id=ID)
    update_wals.execute(id=LANGUAGE, genus_id=ID)


def downgrade():
    pass
