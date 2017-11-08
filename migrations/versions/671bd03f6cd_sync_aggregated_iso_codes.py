# coding=ascii
"""sync aggregated iso_codes

Revision ID: 671bd03f6cd
Revises: 2aa5ce3fe15
Create Date: 2017-11-08 15:59:33.101000

"""
from __future__ import unicode_literals

# revision identifiers, used by Alembic.
revision = '671bd03f6cd'
down_revision = u'2aa5ce3fe15'

import datetime

from alembic import op
import sqlalchemy as sa

# https://github.com/clld/wals-data/issues/134


def upgrade():
    conn = op.get_bind()

    iso_codes = (
        "SELECT COALESCE(string_agg(i.name, ', ' ORDER BY i.name), '') "
        "FROM identifier AS i JOIN languageidentifier AS li "
        "ON li.identifier_pk = i.pk "
        "WHERE i.type = 'iso639-3' AND li.language_pk = w.pk")

    update_w = sa.text(
        'UPDATE walslanguage AS w SET iso_codes = (%s) '
        'WHERE iso_codes != (%s)' % (iso_codes, iso_codes))

    print(conn.execute(update_w).rowcount)


def downgrade():
    pass
