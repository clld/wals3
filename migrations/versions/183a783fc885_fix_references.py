# coding=ascii
"""fix references

Revision ID: 183a783fc885
Revises: 46ce856ab6e
Create Date: 2017-10-18 14:34:27.064000

"""
from __future__ import unicode_literals

# revision identifiers, used by Alembic.
revision = '183a783fc885'
down_revision = u'46ce856ab6e'

import datetime

from alembic import op
import sqlalchemy as sa


ID_BEFORE_AFTER = {
    'Arnasonar-1980': {
        'author': ('\xc1\x81rnasonar, K.  R.', '\xc1rnason, K.  R.'),
        'name': ('\xc1rnasonar 1980', '\xc1rnason 1980'),
        
    },
    'Buenrostros-1991': {
        'author': ('Buenrostros, Christina', 'Buenrostro, Christina'),
        'name': ('Buenrostros 1991', 'Buenrostro 1991'),
    },
    'Muller-1858': {
        'author': ('Muller, F.', 'Hardeland, August'),
        'name': ('Muller 1858', 'Hardeland 1858'),
        'publisher': ('C. A. Spin and son', ' Frederik Muller'),
        'title': (
            'Versuch einer Grammatik der Dajakschen Sprache',
            'Versuch einer Grammatik der Dajackschen Sprache'
        ),
    },
    'Camargo-Bigot-1992': {
        'year': ('1992', '1991'),
    },
    'Kuzmenkov-et-al-2007': {
        'author': (
            'Kuzmenkov, Evgenij A. and Yakhontova, Natalija S. and Nedjalkov, Vladimir P.',
            'Vladimir P. Nedjalkov and Elena K. Skribnik and Evgenij A. Kuzmenkov and Natalija S.Yakhontova'
        ),
        'name': ('Kuzmenkov et al. 2007', 'Nedjalkov et al. 2007'),
        'title': (
            'Reciprocal, sociative, and assistive constructions in Buryat and Khalkha-Mongol',
            'Reciprocal, sociative, comitative and assistive constructions in Buryat and Khalkha-Mongol'
        ),
        'booktitle': (
            'Typology of reciprocal constructions',
            'Reciprocal constructions'
        ),
        'pages': ('1281-1349', '1281-1348'),
    }
}


def upgrade():
    cols = ['id'] + sorted({name for fields in ID_BEFORE_AFTER.values() for name in fields})
    source=sa.table('source', *map(sa.column, cols))
    for id_, fields in sorted(ID_BEFORE_AFTER.items()):
        update = sa.update(source)\
            .where(source.c.id == id_)\
            .where(sa.and_(source.c[f] == before for f, (before, _) in fields.items()))\
            .values({f: after for f, (_, after) in fields.items()})
        op.execute(update)


def downgrade():
    pass
