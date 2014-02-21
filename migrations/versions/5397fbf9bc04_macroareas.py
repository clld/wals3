# coding=utf-8
"""schema migrations to introduce macroareas.

Revision ID: 5397fbf9bc04
Revises: 30e629e24660
Create Date: 2014-01-21 10:51:42.307243

"""

# revision identifiers, used by Alembic.
revision = '5397fbf9bc04'
down_revision = u'30e629e24660'

from datetime import datetime

from alembic import op
import sqlalchemy as sa

from clld.db.meta import JSONEncodedDict


def upgrade():
    op.create_table(
        'macroarea',
        sa.Column('pk', sa.Integer, primary_key=True),
        sa.Column('created', sa.DateTime(timezone=True), default=datetime.utcnow),
        sa.Column('updated', sa.DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow),
        sa.Column('active', sa.Boolean, default=True),
        sa.Column('jsondata', JSONEncodedDict),
        sa.Column('id', sa.String, unique=True),
        sa.Column('name', sa.Unicode),
        sa.Column('description', sa.Unicode),
        sa.Column('markup_description', sa.Unicode),
    )

    op.create_table(
        'languagemacroarea',
        sa.Column('pk', sa.Integer, primary_key=True),
        sa.Column('created', sa.DateTime(timezone=True), default=datetime.utcnow),
        sa.Column('updated', sa.DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow),
        sa.Column('active', sa.Boolean, default=True),
        sa.Column('jsondata', JSONEncodedDict),

        sa.Column('macroarea_pk', sa.Integer, sa.ForeignKey('macroarea.pk')),
        sa.Column('language_pk', sa.Integer, sa.ForeignKey('language.pk')),
    )

    op.create_unique_constraint(
        "languagemacroarea_macroarea_pk_language_pk_key",
        "languagemacroarea",
        ['macroarea_pk', 'language_pk'])


def downgrade():
    op.drop_table('languagemacroarea')
    op.drop_table('macroarea')
