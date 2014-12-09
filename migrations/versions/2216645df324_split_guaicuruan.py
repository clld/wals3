# coding=utf-8
"""split Guaicuruan

Revision ID: 2216645df324
Revises: 7354edfa762
Create Date: 2014-12-09 14:59:28.816000

"""

# revision identifiers, used by Alembic.
revision = '2216645df324'
down_revision = '7354edfa762'

import datetime

from alembic import op
import sqlalchemy as sa

FAMILY_ID = OLD_GENUS = 'guaicuruan'
GENERA = [u'Kadiw\xe9u', u'South Guaicuruan']
GIDS = ['kadiweu', 'southguaicuruan']
ICONS = ['t009900', 'tff6600']
LANGUAGES = [('kdw',), ('abi', 'mcv', 'pga', 'tob')]


def upgrade():
    conn = op.get_bind()

    exists_genus = sa.text('SELECT EXISTS (SELECT 1 FROM genus WHERE id = :id)',
        conn)

    select_family = sa.text('SELECT pk FROM family WHERE id = :id', conn)

    insert_genus = sa.text('INSERT INTO genus '
        '(created, updated, active, id, name, family_pk, icon) VALUES '
        '(now(), now(), true, :id, :name, :family_pk, :icon)', conn)

    update_lang = sa.text('UPDATE language AS l SET updated = now() '
        'WHERE id = :id AND EXISTS (SELECT 1 FROM walslanguage WHERE pk = l.pk '
        'AND genus_pk != (SELECT pk FROM genus WHERE id = :genus_id))', conn)

    update_wals = sa.text('UPDATE walslanguage SET genus_pk = '
        '(SELECT pk FROM genus WHERE id = :genus_id) '
        'WHERE pk = (SELECT pk FROM language WHERE id = :id) '
        'AND genus_pk != (SELECT pk FROM genus WHERE id = :genus_id)', conn)

    insert_config = sa.text('INSERT INTO config (created, updated, active, key, value) '
        'VALUES (now(), now(), true, :key, :value)', conn)
    
    delete_genus = sa.text('DELETE FROM genus WHERE id = :id', conn)

    for name, id, icon, languages in zip(GENERA, GIDS, ICONS, LANGUAGES):
        if not exists_genus.scalar(id=id):
            insert_genus.execute(id=id, name=name, icon=icon,
                family_pk=select_family.scalar(id=FAMILY_ID))
        for wals in languages:
            update_lang.execute(id=wals, genus_id=id)
            update_wals.execute(id=wals, genus_id=id)

    insert_config.execute(key='__Genus_%s__' % OLD_GENUS, value='__gone__')
    delete_genus.execute(id=OLD_GENUS)


def downgrade():
    pass
