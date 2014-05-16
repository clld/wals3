# coding=utf-8
"""cleanup cree

Revision ID: 9c372bf1987
Revises: 286d065b4dc6
Create Date: 2014-05-16 20:56:31.264630

"""

# revision identifiers, used by Alembic.
revision = '9c372bf1987'
down_revision = u'286d065b4dc6'

import datetime

from alembic import op
import sqlalchemy as sa

from clld.db.migration import Connection
from clld.db.models.common import Language, LanguageIdentifier, Identifier


def upgrade():
    conn = Connection(op.get_bind())

    pk = conn.pk(Language, 'cea')
    for li in conn.all(LanguageIdentifier, language_pk=pk):
        id_ = conn.first(Identifier, pk=li.identifier_pk)
        if (id_.name, id_.type) in [
            ('East Cree', 'name'),
            ('crj', 'iso639-3'),
            ('Cree, Southern East', 'name'),
        ]:
            conn.delete(LanguageIdentifier, pk=li.pk)


def downgrade():
    pass
