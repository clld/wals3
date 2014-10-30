# coding=utf-8
"""fix alternative names

Revision ID: 354b3934b053
Revises: 1df16a574334
Create Date: 2014-10-30 12:24:22.718000

"""

# revision identifiers, used by Alembic.

revision = '354b3934b053'
down_revision = '1df16a574334'

import datetime

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute("DELETE FROM languageidentifier AS li "
        "WHERE EXISTS (SELECT 1 FROM identifier "
            "WHERE pk = li.identifier_pk "
            "AND (name IS NULL OR name = '' "
            "OR name ~ '^Identifier [a-z]{3} has been changed$'))")

    op.execute("DELETE FROM identifier "
        "WHERE name IS NULL OR name = '' "
        "OR name ~ '^Identifier [a-z]{3} has been changed$'")


def downgrade():
    pass
