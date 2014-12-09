# coding=utf-8
"""fix datapoint sources trr

Revision ID: 52167a1500ca
Revises: 245924ef4e97
Create Date: 2014-12-09 17:07:55.726000

"""

# revision identifiers, used by Alembic.
revision = '52167a1500ca'
down_revision = '245924ef4e97'

import datetime

from alembic import op
import sqlalchemy as sa


def upgrade():
    conn = op.get_bind()

    update_pages = sa.text('UPDATE valuesetreference AS r SET updated = now(), '
        'description = :after WHERE description = :before '
        'AND EXISTS (SELECT 1 FROM valueset WHERE pk = r.valueset_pk '
        'AND id = :id) '
        'AND EXISTS (SELECT 1 FROM source WHERE pk = r.source_pk '
        'AND id = :ref)', conn)

    insert_source = sa.text('INSERT INTO valuesetreference '
        '(created, updated, active, version, valueset_pk, source_pk, description) '
        'VALUES (now(), now(), true, 1, '
            '(SELECT pk FROM valueset WHERE id = :id), '
            '(SELECT pk FROM source WHERE id = :ref), '
        ':pages)', conn)

    update_source = sa.text('UPDATE valuesetreference AS r SET updated = now(), '
        'source_pk = (SELECT pk FROM source WHERE id = :after) '
        'WHERE source_pk = (SELECT pk FROM source WHERE id = :before) '
        'AND EXISTS (SELECT 1 FROM valueset WHERE pk = r.valueset_pk '
        'AND id = ANY(:ids))', conn)

    update_pages.execute(id='69A-trr', ref='Vincent-1973a',
        before='531, 563', after='531')
    insert_source.execute(id='69A-trr', ref='Vincent-1973b',
        pages='563')

    update_pages.execute(id='101A-trr', ref='Vincent-1973a',
        before='535, 563', after='535')
    insert_source.execute(id='101A-trr', ref='Vincent-1973b',
        pages='563')

    update_source.execute(before='Vincent-1973a', after='Vincent-1973b',
        ids=['112A-trr',
             '143A-trr', '143E-trr', '143F-trr', '143G-trr',
             '144A-trr', '144B-trr', '144L-trr', '144P-trr', '144Q-trr',
             '144R-trr', '144S-trr'])


def downgrade():
    pass
