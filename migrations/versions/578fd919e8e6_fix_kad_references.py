# coding=utf-8
"""fix kad references

Revision ID: 578fd919e8e6
Revises: 5048aaa71fe
Create Date: 2014-12-01 15:39:27.730000

"""

# revision identifiers, used by Alembic.
revision = '578fd919e8e6'
down_revision = '5048aaa71fe'

import datetime

from alembic import op
import sqlalchemy as sa


def upgrade():
    update = sa.text("UPDATE source SET updated = now(), "
        "author = :after, title = :title, description = :title, "
        "name = concat_ws(' ', substring(:after from '\w+'), year), "
        "series = :series, volume = :volume, publisher = :publisher "
        "WHERE id = :id AND author = :before").bindparams(
            before='Abdalla, Abdalla Ibrahim',
            after='Kutoado, Abdalla Ibrahim Abdalla',
            title='Kadugli language and language usage',
            series=None, volume=None,
            publisher='Institute of African and Asian Studies, University of Khartoum')
    
    op.execute(update.bindparams(id='Abdalla-1969'))
    op.execute(update.bindparams(id='Abdalla-1973'))


def downgrade():
    pass
