# coding=utf-8
"""july 2014

Revision ID: 12dbc8689bb
Revises: 9c372bf1987
Create Date: 2014-07-03 09:43:04.393266

"""
from __future__ import unicode_literals

# revision identifiers, used by Alembic.
revision = '12dbc8689bb'
down_revision = '9c372bf1987'

import datetime

from alembic import op
import sqlalchemy as sa
from clld.db.migration import Connection
from clld.db.models.common import (
    Language, Source, Sentence, Identifier, LanguageIdentifier,
)

from wals3.models import WalsLanguage, Genus, Family


def upgrade():
    conn = Connection(op.get_bind())

   # We need to change the name of Kaliai-Kove (kkv) to Lusi (which is the Glottolog name).
    pk = conn.pk(Language, 'kkv')
    conn.update(Language, [('name', 'Lusi')], pk=pk)
    conn.update(WalsLanguage, [('ascii_name', 'lusi'), ('iso_codes', 'khl')], pk=pk)
    #wals3=# select li.pk, i.name, i.type, i.description from languageidentifier as li, identifier as i where li.language_pk = 2163 and li.identifier_pk = i.pk;
    #  pk   |     name     |   type    | description
    #-------+--------------+-----------+-------------
    #  1302 | Kove         | name      | ruhlen
    #  2749 | Kove-Kaliai  | name      | routledge
    #  4202 | Kaliai       | name      | other
    #  4406 | Kandoka-Lusi | name      | other
    #  4901 | Kaliai Kove  | name      | other
    #  7797 | khl          | iso639-3  | Lusi
    #  7798 | kvc          | iso639-3  | Kove
    # 10488 | Lusi         | name      | ethnologue
    # 10489 | Kove         | name      | ethnologue
    # 13658 | kali1298     | glottolog |
    conn.update(Identifier, [('name', 'lusi1240')], name='kali1298')
    remove = []
    for row in conn.execute("""
select li.pk, i.name from languageidentifier as li, identifier as i
where li.language_pk = %s and li.identifier_pk = i.pk""" % pk):
        if 'Kove' in row['name'] or row['name'] == 'kvc':
            remove.append(row['pk'])
    for pk in remove:
        conn.delete(LanguageIdentifier, pk=pk)

    # The language Dizi (wals code diz) needs to be removed from North Omotic and placed in a
    # separate (new) genus called Dizoid, within the Omotic subfamily of Afro-Asiatic.
    # (Glottolog actually treats Dizoid as a separate family altogether, which is good reason
    # to conclude that it is at least a separate genus.)
    pk = conn.pk(Family, 'afroasiatic')
    dizoid = conn.insert(
        Genus,
        id='dizoid',
        name='Dizoid',
        family_pk=pk,
        subfamily='Omotic',
        icon='tdd0000')
    pk = conn.pk(Language, 'diz')
    conn.update(WalsLanguage, [('genus_pk', dizoid)], pk=pk)

    # The name for what is now Siraiya (sry) should be changed to Siraya. (Siraya is also the Glottolog name)
    pk = conn.pk(Language, 'sry')
    conn.update(Language, [('name', 'Siraya')], pk=pk)
    conn.update(WalsLanguage, [('ascii_name', 'siraya')], pk=pk)

    # I want to modify the assignment of languages to genera for the Austronesian languages of Taiwan.
    # (This change brings WALS in line with Glottolog.)  Namely, I want to split up the current Paiwanic genus as follows:
    #
    # - Amis and Siraya should be moved into a new genus called East Formosan.
    # - Thao should be moved into a new genus called Western Plains Austronesian.
    #
    paiwanic = conn.first(Genus, id='paiwanic')
    eastformosan = conn.insert(
        Genus,
        id='eastformosan',
        name='East Formosan',
        family_pk=paiwanic['family_pk'],
        icon='fdd0000')
    westernplainsaustronesian = conn.insert(
        Genus,
        id='westernplainsaustronesian',
        name='Western Plains Austronesian',
        family_pk=paiwanic['family_pk'],
        icon='f0000dd')
    for lid in ['ami', 'sry']:
        pk = conn.pk(Language, lid)
        conn.update(WalsLanguage, [('genus_pk', eastformosan)], pk=pk)
    pk = conn.pk(Language, 'thw')
    conn.update(WalsLanguage, [('genus_pk', westernplainsaustronesian)], pk=pk)

    # The sole remaining language in Paiwanic is Paiwan, but since this genus now contains only one language,
    # we should rename the genus Paiwan.
    conn.update(Genus, [('name', 'Paiwan')], id='paiwanic')

    # For similar reasons, the genus Tsouic should just be called Tsou.
    conn.update(Genus, [('name', 'Tsou')], id='tsouic')

    # The genus currently called Southern Atlantic should be renamed Mel.  (This brings it in line with Glottolog.)
    conn.update(Genus, [('name', 'Mel')], id='southernatlantic')


    for id in ['Ashton-1947', 'Ashton-1969']:
        pk = conn.pk(Source, id)
        conn.update(Source, [('author', 'Ethel O. Ashton')], pk=pk)

    pk = conn.pk(Source, 'Poldaufem-1971')
    conn.update(
        Source,
        [
            ('name', 'Poldauf 1971'),
            ('author', 'Poldauf, Ivan'),
            ('description', 'Anglicko-český a česko-anglický slovník'),
            ('title', 'Anglicko-český a česko-anglický slovník'),
        ],
        pk=pk)

    #wals3=# select author, name, pages, title, description from source where id = 'De-Lancey-2003';
    #      author      |      name      |  pages  |       title       |    description
    #------------------+----------------+---------+-------------------+-------------------
    # De Lancey, Scott | De Lancey 2003 | 255-269 | Classical Tibetan | Classical Tibetan
    #(1 row)
    #-> DeLancey                           270-288  Lhasa Tibetan
    pk = conn.pk(Source, 'De-Lancey-2003')
    conn.update(
        Source,
        [
            ('name', 'DeLancey 2003'),
            ('author', 'DeLancey, Scott'),
            ('description', 'Lhasa Tibetan'),
            ('title', 'Lhasa Tibetan'),
        ],
        pk=pk)

    pk = conn.pk(Source, 'Frajzyngier-and-Shay-2002')
    conn.update(Source, [('author', 'Frajzyngier, Zygmunt with Erin Shay')], pk=pk)

    # wals-data #9
    conn.execute("update domainelement set name = 'No voicing contrast' where name = 'No voicing constrast'")

    # wals-data #7
    pk = conn.pk(Source, 'Brown-1990')
    conn.update(
        Source,
        [
            ('description', 'Mai Brat Nominal Phrases'),
            ('title', 'Mai Brat Nominal Phrases'),
            ('booktitle', 'Miscellaneous Studies of Indonesian and Other Languages of Indonesia, Part X'),
        ],
        pk=pk)

    pk = conn.pk(Source, 'Saltarelli-et-al-1988')
    conn.update(
        Source,
        [('author',
          'Saltarelli, Mario with Miren Azkarate,  and Farwell, David and de Urbina, Jon Ortiz and Oñederra, Lourdes')],
        pk=pk)

    #wals3=# select xhtml from sentence where id = '478';
    #replace:
    #'anywhere' -> 'whenever'
    #'where' -> 'when'
    res = conn.first(Sentence, id='478')
    xhtml = res['xhtml']
    for s, r in [("'anywhere'", "'whenever'"), ("'where'", "'when'")]:
        assert s in xhtml
        xhtml = xhtml.replace(s, r)
    conn.update(Sentence, [('xhtml', xhtml)], id='478')


def downgrade():
    pass
