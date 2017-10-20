# coding=utf-8
"""fix references with control characters

Revision ID: 45055609733c
Revises: 52f817261005
Create Date: 2017-10-20 11:08:42.949000

"""
from __future__ import unicode_literals

# revision identifiers, used by Alembic.
revision = '45055609733c'
down_revision = u'52f817261005'

import datetime

from alembic import op
import sqlalchemy as sa

CC_RE = '[\\u0000-\\u001f\\u007f-\\u009f]'

ID_BEFORE = {  # https://github.com/clld/wals-data/issues/131
    'Andreasen-and-Dahl-1998': {
        'author': 'Andreasen, Paulivar and Dahl, Á\x81rni',
    },
    'Arnason-1999': {
        'author': 'Á\x81rnason, Kristján',
    },
    'Birtalan-2003': {
        'author': 'Birtalan, Á\x81gnes',
    },
    'Csato-and-Karakoc-1998': {
        'editor': 'Johanson, Lars and Csató, Éva Ã\x81.',
    },
    'Feev-1998': {
        'description': 'Akustich\x8deskie xarakteristiki glasnyx ketskogo jazyka (Pakulixinskij govor)',
        'title': 'Akustich\x8deskie xarakteristiki glasnyx ketskogo jazyka (Pakulixinskij govor)',
    },
    'Fukushima-1991': {
        'description': 'The Proper Treatment of "Every"\x9d and "Some"\x9d in Japanese',
        'title': 'The Proper Treatment of "Every"\x9d and "Some"\x9d in Japanese',
    },
    'Gadzhiaxmedov-2000': {
        'address': 'Maxach\x8dkala',
    },
    'GrandEury-1991': {
        'author': 'Grand\x92Eury, Sylvie',
    },
    'Haan-2001': {
        'description': 'The grammar of Adang: a Papuan language spoken on the Island of Alor, East Nusa Tenggara \x96 Indonesia',
        'title': 'The grammar of Adang: a Papuan language spoken on the Island of Alor, East Nusa Tenggara \x96 Indonesia',
    },
    'Harrison-et-al-1981': {
        'series': 'Serie de vocabularios y diccionarios indígenas "Mariano Silva y Aceves"\x9d',
    },
    'Hazoume-1979': {
        'description': 'Etude descriptive du \x91Gungbe\x92',
        'title': 'Etude descriptive du \x91Gungbe\x92',
    },
    'Jacquesson-2005': {
        'description': 'Le deuri: langue tibéto-birmane d\x92Assam',
        'title': 'Le deuri: langue tibéto-birmane d\x92Assam',
    },
    'Jakovlev-1940': {
        'description': 'Sintakisis ch\x8dech\x8denskogo literaturnogo jazyka',
        'title': 'Sintakisis ch\x8dech\x8denskogo literaturnogo jazyka',
    },
    'Kirchner-1998a': {
        'editor': 'Johanson, Lars and Csató, Éva Á\x81.',
    },
    'Kirchner-1998b': {
        'editor': 'Johanson, Lars and Csató, Éva Á\x81.',
    },
    'Klimov-1970': {
        'author': 'Klimov, Georgij Andreevich\x8d',
    },
    'Koval-1979': {
        'description': 'O znachenii morfologich\x8deskogo pokazatelja klassa v fula',
        'title': 'O znachenii morfologich\x8deskogo pokazatelja klassa v fula',
    },
    'Nguyen-1966': {
        'author': 'Nguyen, D\x90inh-Hoa',
    },
    'Russell-1999': {
        'description': "The 'Word'\x9d in two Polysynthetic Languages",
        'title': "The 'Word'\x9d in two Polysynthetic Languages",
    },
    'Schonig-1998a': {
        'editor': 'Johanson, Lars and Csató, Éva Á\x81.',
    },
    'Schonig-1998b': {
        'editor': 'Johanson, Lars and Csató, Éva Á\x81.',
    },
    'Tchitchi-1984': {
        'description': 'Systématique de l\x92Ajagbe',
        'title': 'Systématique de l\x92Ajagbe',
    },
    'Ucida-1970': {
        'author': 'Uc\x8dida, Norihiko',
    },
    'Werner-1993': {
        'description': 'Tìdn-Á\x81al: A Study of Midob (Darfur-Nubian)',
        'title': 'Tìdn-Á\x81al: A Study of Midob (Darfur-Nubian)',
    },
    'Wetshemongo-1996': {
        'description': 'Systématique grammaticale de l\x92otetela, langue bantu de Zaire',
        'title': 'Systématique grammaticale de l\x92otetela, langue bantu de Zaire',
    },
    'Xajdakov-1963': {
        'description': "Principy raspredelenija imen sushch\x8destvitel'nyx po grammatich\x8deskim klassam v lakskom jazyke",
        'title': "Principy raspredelenija imen sushch\x8destvitel'nyx po grammatich\x8deskim klassam v lakskom jazyke",
    },
}


def upgrade():
    cols = ['id', 'updated'] + sorted({name for fields in ID_BEFORE.values() for name in fields})
    source = sa.table('source', *map(sa.column, cols))
    for id_, fields in sorted(ID_BEFORE.items()):
        update = sa.update(source)\
            .where(source.c.id == id_)\
            .where(sa.and_(source.c[f] == before for f, before in fields.items()))\
            .values(updated=sa.func.now())\
            .values({f: sa.func.regexp_replace(source.c[f], CC_RE, '', 'g') for f in fields})
        op.execute(update)


def downgrade():
    pass
