# coding=utf-8
"""reclassify yzv

Revision ID: 547d1f4ea331
Revises: 354b3934b053
Create Date: 2014-11-12 09:41:00.011000

"""

# revision identifiers, used by Alembic.

revision = '547d1f4ea331'
down_revision = '354b3934b053'

import datetime

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute(sa.text('UPDATE language AS l SET updated = now() '
        'WHERE id = :id AND EXISTS (SELECT 1 FROM walslanguage WHERE pk = l.pk '
            'AND genus_pk = (SELECT pk FROM genus WHERE id = :before))'
        ).bindparams(id='yzv', before='finnic'))
    op.execute(sa.text('UPDATE walslanguage AS w '
        'SET genus_pk = (SELECT pk FROM genus WHERE id = :after) '
        'WHERE genus_pk = (SELECT pk FROM genus WHERE id = :before) '
        'AND EXISTS (SELECT 1 FROM language WHERE pk = w.pk AND id = :id)'
        ).bindparams(id='yzv', before='finnic', after='permic'))


def downgrade():
    pass
