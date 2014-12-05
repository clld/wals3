# coding=utf-8
"""new contact address

Revision ID: 345997083bc4
Revises: 578fd919e8e6
Create Date: 2014-12-05 11:05:41.966000

"""

# revision identifiers, used by Alembic.
revision = '345997083bc4'
down_revision = '578fd919e8e6'

import datetime

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute(sa.text('UPDATE dataset SET updated = now(), '
        'contact = :after WHERE id = :id AND contact = :before'
        ).bindparams(id='wals', before='contact.wals@livingreviews.org',
            after='wals@eva.mpg.de'))


def downgrade():
    pass
