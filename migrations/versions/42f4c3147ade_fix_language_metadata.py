# coding=utf-8
"""fix language metadata

Revision ID: 42f4c3147ade
Revises: 4d7c16d2157a
Create Date: 2015-10-09 10:00:55.298295

"""
from __future__ import unicode_literals

# revision identifiers, used by Alembic.
revision = '42f4c3147ade'
down_revision = '4d7c16d2157a'

import datetime

from alembic import op
import sqlalchemy as sa

from wals3.migration import Connection


def upgrade():
    conn = Connection(op.get_bind())
    # https://github.com/clld/wals-data/issues/64
    conn.update_name('bnr', 'Bilinarra')
    conn.update_source(
        'Nordlinger-1990',
        description='A Sketch Grammar of Bilinarra',
        title='A Sketch Grammar of Bilinarra')

    # https://github.com/clld/wals-data/issues/63
    conn.update_name('jva', 'Karajá')
    conn.update_name('ghr', 'Bunan')

    # https://github.com/clld/wals-data/issues/59
    conn.update_genus('lrd', 'tangkic')

    # https://github.com/clld/wals-data/issues/54
    conn.update_source(
        'Schauer-and-Schauer-1958',
        name='Schauer and Schauer 1978',
        year='1978',
        year_int=1978)

    # https://github.com/clld/wals-data/issues/53
    conn.update_genus(
        'ocu', ('matlatzincan', 'Matlatzincan', 't9999ff'), family='otomanguean')

    # https://github.com/clld/wals-data/issues/47
    conn.update_name('bno', 'Waimaha')

    # https://github.com/clld/wals-data/issues/46
    conn.update_source(
        'Troike-1996',
        booktitle='Handbook of North American Indians. Volume 17: Languages')

    # https://github.com/clld/wals-data/issues/42
    conn.update_name('cos', 'Rumsien')


def downgrade():
    pass
