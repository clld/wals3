# coding=utf-8
"""fix lost sources

Revision ID: 4417c4a41762
Revises: 58559d4eea0d
Create Date: 2015-08-03 09:41:58.492074

"""

# revision identifiers, used by Alembic.
revision = '4417c4a41762'
down_revision = u'58559d4eea0d'

import datetime

from alembic import op
import sqlalchemy as sa

from clld.db.models.common import ValueSet, ValueSetReference, Source
from clld.db.migration import Connection


#
# The following two ValueSetReferences lost the source relation in the 2013 upgrade, when
# fixing issues https://github.com/clld/wals3/issues/28 and
# https://github.com/clld/wals3/issues/27
#
VALUESETREFERENCES = [
    ('53A', 'kug', 'Gui-2000'),
    ('40A', 'kon', 'Lumwamu-1973'),
]


def upgrade():
    conn = Connection(op.get_bind())
    for fid, lid, sid in VALUESETREFERENCES:
        vs = conn.pk(ValueSet, '%s-%s' % (fid, lid))
        s = conn.pk(Source, sid)
        conn.update(ValueSetReference, dict(source_pk=s), valueset_pk=vs, source_pk=None)

    assert not list(conn.select(ValueSetReference, source_pk=None))


def downgrade():
    pass
