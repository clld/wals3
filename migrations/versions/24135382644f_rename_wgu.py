# coding=utf-8
"""rename wgu

Revision ID: 24135382644f
Revises: 3845ae1142f3
Create Date: 2015-04-28 12:12:11.368000

"""

# revision identifiers, used by Alembic.
revision = '24135382644f'
down_revision = '3845ae1142f3'

import datetime

from alembic import op
import sqlalchemy as sa

ID, BEFORE, AFTER = 'wgu', 'Warrungu', 'Warrongo'


def upgrade():
    update_name = sa.text('UPDATE language SET updated = now(), '
        'name = :after WHERE id = :id AND name = :before')

    params = {'type': 'name', 'description': 'other', 'lang': 'en'}

    insert_ident = sa.text('INSERT INTO identifier '
        '(created, updated, active, version, type, description, lang, name) '
        'SELECT now(), now(), true, 1, :type, :description, :lang, :name '
        'WHERE NOT EXISTS (SELECT 1 FROM identifier WHERE type = :type '
        'AND description = :description AND lang = :lang AND name = :name)'
        ).bindparams(**params)

    insert_lang_ident = sa.text('INSERT INTO languageidentifier '
        '(created, updated, active, version, language_pk, identifier_pk) '
        'SELECT now(), now(), true, 1, '
        '(SELECT pk FROM language WHERE id = :id), '
        '(SELECT pk FROM identifier WHERE type = :type '
        'AND description = :description AND lang = :lang AND name = :name) '
        'WHERE NOT EXISTS (SELECT 1 FROM languageidentifier '
        'WHERE language_pk = (SELECT pk FROM language WHERE id = :id) '
        'AND identifier_pk = (SELECT pk FROM identifier WHERE type = :type '
        'AND description = :description AND lang = :lang AND name = :name))'
        ).bindparams(**params)

    op.execute(update_name.bindparams(id=ID, before=BEFORE, after=AFTER))
    op.execute(insert_ident.bindparams(name=BEFORE))
    op.execute(insert_lang_ident.bindparams(id=ID, name=BEFORE))
    

def downgrade():
    pass
