from __future__ import unicode_literals
import sys
import transaction
from itertools import groupby, cycle
import re
from datetime import date, datetime

from pytz import utc
from sqlalchemy import create_engine
from path import path

from clld.db.meta import DBSession, VersionedDBSession
from clld.db.models import common
from clld.db.util import compute_language_sources
from clld.scripts.util import initializedb, Data
from clld.lib.bibtex import EntryType
from clld.lib.dsv import rows

import wals3
from wals3 import models
from wals3.scripts import uncited


UNCITED_MAP = {}
for k, v in uncited.MAP.items():
    UNCITED_MAP[k.lower()] = v

# start with what's online right now:
DB = create_engine('postgresql://robert@/wals-vm42')
REFDB = create_engine('postgresql://robert@/walsrefs')

ABBRS = {
    "A": "agent-like argument",
    "ACCOMP": "accompanied ",
    "ACR": "actor",
    "ACT": "actual",
    "ADEL": "adelative",
    "ADVZ": "adverbializer",
    "AFF": "affirmative",
    "AGT": "agent",
    "ALL": "allative",
    "AN": "action nominal",
    "ANC": "action nominal construction",
    "ANIM": "animate",
    "ANTIP": "antipassive",
    "APPL": "applicative",
    "AS": "asseverative",
    "ASSOC": "associative",
    "ASY": "asymmetric",
    "ATTR": "attributive",
    "AUD": "auditory evidential",
    "AUG": "augmented",
    "C": "common gender",
    "CL": "class (= noun class, gender)",
    "CLF": "classifier",
    "CMPL": "completive",
    "CNTR": "contrary to expectation marker",
    "COLL": "collective",
    "COM": "comitative",
    "COMPR": "comparative",
    "CONN": "connective",
    "CONNEG": "connegative",
    "CONSTR": "construct",
    "CONT": "continuative, continous",
    "CONTEMP": "contemporative",
    "COP": "copula",
    "CPW": "categories per word",
    "CRS": "currently relevant state",
    "DECL": "declarative",
    "DEG": "degree word",
    "DEP": "dependent marker",
    "DES": "desire",
    "DESID": "desiderative",
    "DIM": "diminutive",
    "DIR": "direct",
    "DIR.EVD": "direct evidential",
    "DIRL": "directional",
    "DIST.PST": "distant past",
    "DOBJ": "direct object",
    "DS": "different subject",
    "EMPH": "emphatic",
    "EPENTH": "epenthetic",
    "EPV": "expletive verbal suffix",
    "EVD": "evidential",
    "FACT": "fact",
    "FAM": "familiar",
    "FIN": "finite",
    "FIN.AOR": "finite aorist",
    "FV": "verb-final vowel",
    "HAB": "habitual",
    "HEST": "hesternal past",
    "HHON": "super honorific",
    "HOD": "hodiernal past",
    "HON": "honorific",
    "HORT": "hortative",
    "HUM": "human",
    "IE": "Indo-European",
    "ILL": "illative",
    "IMM.PRET": "immediate preterite",
    "IMM.PST": "immediate past",
    "IMPERS": "impersonal",
    "INAN": "inanimate",
    "INCEP": "inceptive",
    "INCOMPL": "incompletive",
    "IND": "indicative",
    "INDIR.EVD": "indirect evidential",
    "INFER": "inferential evidential",
    "INGR": "ingressive",
    "INTENT": "intentional",
    "INTER": "interrogative",
    "INTF": "intensifier",
    "INTGEN": "intended genitive",
    "INV": "inverse",
    "IO": "indirect object ",
    "IRR": "irrealis",
    "ITER": "iterative",
    "LIG": "ligature",
    "LOCUT": "locutor person marker",
    "MED": "medial",
    "NARR": "narrative",
    "NC": "noun class",
    "NEC": "necessity",
    "NHON": "non-honorific",
    "NOMIN": "nominalization",
    "NON.F": "non-feminine ",
    "NONFIN": "non-finite ",
    "NONFIN.AOR": "non-finite aorist",
    "NP": "noun phrase",
    "NPST": "non-past",
    "NSG": "non-singular",
    "NUM": "numeral",
    "O": "object pronominal marker",
    "OBV": "obviative",
    "OPT": "optative",
    "P": "patient-like argument",
    "PAT": "patient",
    "PATH": "path locative",
    "PCL": "particle",
    "PERS": "personal",
    "PHR.TERM": "phrase terminal marker",
    "PLUPERF": "pluperfect",
    "POS": "possibility",
    "POSTP": "postposition",
    "POT": "potential",
    "PP": "prepositional/postpositional phrase",
    "PRECONTEMP": "precontemporal",
    "PRED": "predicative",
    "PREF": "prefix",
    "PREP": "preposition",
    "PREV": "preverb",
    "PROL": "prolative",
    "PRON": "pronoun",
    "PROP": "proper name",
    "PRTV": "partitive",
    "PST.CONT": "past continuous",
    "PST.PUNCT": "past punctiliar",
    "PSTBEFOREYEST": "past before yesterday (= prehesternal)",
    "PUNCT": "punctual stem",
    "Q": "question-marker",
    "QUOT": "quotative",
    "RDP": "reduplication",
    "REAL": "realis",
    "REC": "recent (past)",
    "RECP": "reciprocal",
    "REM.PST": "remote past",
    "REMOTE": "remote",
    "REPET": "repetitive",
    "RLZ": "realized",
    "RNR": "result nominalizer",
    "S": "sole argument of the intransitive verb",
    "SBJV": "subjunctive",
    "SENS": "sensory evidential",
    "SPEC": "specific",
    "SR": "switch Reference",
    "SS": "same subject",
    "STAT": "stative",
    "SUBORD": "subordination",
    "SUFF": "suffix",
    "SUP": "superessive",
    "SYM": "symmetric",
    "SymAsy": "symmetric and asymmetric",
    "T/A": "tense/ aspect",
    "TD": "time depth/ proximality marker",
    "TELIC": "telic",
    "TEMPRY": "temporary",
    "TH": "thematic suffix",
    "THM": "theme (i.e. the semantic role)",
    "TOD.PST": "today past",
    "TRASL": "traslative",
    "TRI": "trial",
    "UNSP": "unspecified",
    "VBLZ": "verbalizer",
    "VENT": "ventive",
    "VIS": "visual evidential",
    "VP": "verb phrase",
}


class Icons(object):
    filename_pattern = re.compile('(?P<spec>(c|d|s|f|t)[0-9a-f]{3})\.png')

    @staticmethod
    def id(spec):
        return ''.join(c if i == 0 else c + c for i, c in enumerate(spec))

    def __init__(self):
        self._icons = []
        for name in sorted(
            path(wals3.__file__).dirname().joinpath('static', 'icons').files()
        ):
            m = self.filename_pattern.match(name.splitall()[-1])
            if m:
                self._icons.append(Icons.id(m.group('spec')))

    def __iter__(self):
        return iter(self._icons)


def get_source(id):
    """retrieve a source record from wals_refdb
    """
    field_map = {
        'onlineversion': 'url',
        'gbs_id': 'google_book_search_id',
        'doi': 'jsondata',
        'cited': 'jsondata',
        'conference': 'jsondata',
        'iso_code': 'jsondata',
        'olac_field': 'jsondata',
        'wals_code': 'jsondata',
    }

    res = {'id': id, 'jsondata': {'iso_code': [], 'olac_field': [], 'wals_code': []}}
    refdb_id = UNCITED_MAP.get(id.lower())
    if not refdb_id:
        for row in REFDB.execute("""\
select id, genre from ref_record, ref_recordofdocument
where id = id_r_ref and citekey = '%s'""" % id
        ):
            res['bibtex_type'] = row['genre']
            refdb_id = row['id']
            break

        if not refdb_id:
            if id[-1] in ['a', 'b', 'c', 'd']:
                refdb_id = UNCITED_MAP.get(id[:-1].lower())
            if not refdb_id:
                print 'missing ref', id
                return {}

    if 'bibtex_type' not in res:
        for row in REFDB.execute("select genre from ref_record where id = %s" % refdb_id):
            res['bibtex_type'] = row['genre']
            break

    for row in REFDB.execute(
        "select * from ref_recfields where id_r_ref = %s" % refdb_id
    ):
        field = field_map.get(row['id_name'], row['id_name'])
        if field == 'jsondata':
            if row['id_name'] in ['iso_code', 'olac_field', 'wals_code']:
                res['jsondata'][row['id_name']].append(row['id_value'])
            else:
                res['jsondata'][row['id_name']] = row['id_value']
        else:
            res[field] = row['id_value']

    if res['bibtex_type'] == 'thesis':
        if res['format'] == 'phd':
            res['bibtex_type'] == 'phdthesis'
            del res['format']
        elif res['format'] == 'ma':
            res['bibtex_type'] == 'mastersthesis'
            del res['format']
        else:
            res['bibtex_type'] == 'misc'

    if res['bibtex_type'] == 'online':
        res['howpublished'] = 'online'

    res['bibtex_type'] = getattr(EntryType, res['bibtex_type'], EntryType.misc)
    if 'format' in res:
        res['type'] = res['format']
        del res['format']

    authors = ''
    for row in REFDB.execute(
        "select * from ref_recauthors where id_r_ref = %s order by ord" % refdb_id
    ):
        if row['type'] == 'etal':
            authors += ' et al.'
        else:
            if authors:
                authors += ' and '
            authors += row['value']
    res['author'] = authors

    for row in REFDB.execute(
        "select * from ref_recjournal where id_r_ref = %s" % refdb_id
    ):
        res['journal'] = row['name']
        break

    return res


def get_vs2008(args):
    vs2008 = {}
    for row in rows(args.data_file('datapoints_2008.csv'), delimiter=','):
        vs2008[(row[0], '%sA' % row[1])] = int(row[2])
    return vs2008


E2008 = utc.localize(datetime(2008, 4, 21))
E2011 = utc.localize(datetime(2011, 4, 28))
E2013 = utc.localize(datetime(2013, 8, 31))


def main(args):
    icons = Icons()
    old_db = DB

    data = Data(created=E2008, updated=E2008)
    vs2008 = get_vs2008(args)

    missing_sources = []
    with open('/home/robert/venvs/clld/data/wals-data/missing_source.py', 'w') as fp:
        for row in old_db.execute("select * from reference"):
            try:
                author, year = row['id'].split('-')
            except:
                author, year = None, None
            bibdata = get_source(row['id'])
            if not bibdata:
                fp.write('"%s",\n' % row['id'])
                missing_sources.append(row['id'])

            bibdata.update({
                'id': row['id'],
                'name': row['name'],
                'description': bibdata.get('title', bibdata.get('booktitle')),
                'google_book_search_id': row['gbs_id'] or None,
            })
            data.add(common.Source, row['id'], **bibdata)

        #
        # TODO: add additional bibdata as data items
        #

    print('sources missing for %s refs' % len(missing_sources))

    for id, name in ABBRS.items():
        DBSession.add(common.GlossAbbreviation(id=id, name=name))

    for row in old_db.execute("select * from country"):
        data.add(
            models.Country, row['id'],
            id=row['id'], name=row['name'], continent=row['continent'])

    for row in old_db.execute("select * from family"):
        data.add(
            models.Family, row['id'],
            id=row['id'], name=row['name'], description=row['comment'])

    for row, icon in zip(
        list(old_db.execute("select * from genus order by family_id")),
        cycle(iter(icons))
    ):
        genus = data.add(
            models.Genus, row['id'],
            id=row['id'], name=row['name'], icon=icon, subfamily=row['subfamily'])
        genus.family = data['Family'][row['family_id']]
    DBSession.flush()

    for row in old_db.execute("select * from altname"):
        data.add(common.Identifier, (row['name'], row['type']),
                 name=row['name'], type='name-%s' % row['type'])
    DBSession.flush()

    for row in old_db.execute("select * from isolanguage"):
        data.add(
            common.Identifier, row['id'],
            id=row['id'],
            name=row['name'],
            type=common.IdentifierType.iso.value,
            description=row['dbpedia_url'])
    DBSession.flush()

    for row in old_db.execute("select * from language"):
        kw = dict((key, row[key]) for key in ['id', 'name', 'latitude', 'longitude'])
        lang = data.add(
            models.WalsLanguage, row['id'],
            samples_100=row['samples_100'] != 0,
            samples_200=row['samples_200'] != 0,
            **kw)
        lang.genus = data['Genus'][row['genus_id']]

    for row in old_db.execute("select * from author"):
        data.add(
            common.Contributor, row['id'],
            name=row['name'],
            url=row['www'],
            id=row['id'],
            description=row['note'])
    DBSession.flush()

    dataset = common.Dataset(
        id='wals',
        name='WALS Online',
        description='The World Atlas of Language Structures Online',
        domain='wals.info',
        published=date(2013, 8, 15),
        #license='http://creativecommons.org/licenses/by-sa/3.0/',
        license='http://creativecommons.org/licenses/by-nc-nd/2.0/de/deed.en',
        contact='wals@eva.mpg.de',
        jsondata={
            #'license_icon': 'http://i.creativecommons.org/l/by-sa/3.0/88x31.png',
            #'license_name': 'Creative Commons Attribution-ShareAlike 3.0 Unported License'})
            'license_icon': 'http://wals.info/static/images/cc_by_nc_nd.png',
            'license_name': 'Creative Commons Attribution-NonCommercial-NoDerivs 2.0 Germany'})
    DBSession.add(dataset)

    for i, editor in enumerate(['dryerms', 'haspelmathm']):
        common.Editor(dataset=dataset, contributor=data['Contributor'][editor], ord=i + 1)

    for row in old_db.execute("select * from country_language"):
        DBSession.add(models.CountryLanguage(
            language_pk=data['WalsLanguage'][row['language_id']].pk,
            country_pk=data['Country'][row['country_id']].pk))

    for row in old_db.execute("select * from altname_language"):
        DBSession.add(common.LanguageIdentifier(
            language=data['WalsLanguage'][row['language_id']],
            identifier=data['Identifier'][(row['altname_name'], row['altname_type'])],
            description=row['relation']))
    DBSession.flush()

    for row in old_db.execute("select * from isolanguage_language"):
        DBSession.add(common.LanguageIdentifier(
            language=data['WalsLanguage'][row['language_id']],
            identifier=data['Identifier'][row['isolanguage_id']],
            description=row['relation']))
    DBSession.flush()

    for row in old_db.execute("select * from area"):
        data.add(
            models.Area, row['id'],
            name=row['name'], dbpedia_url=row['dbpedia_url'], id=str(row['id']))
    DBSession.flush()

    #
    # turn supplements into contributions!!
    #
    for row in old_db.execute("select * from chapter"):
        kw = dict(id=row['id'], name=row['name'])
        if int(row['id']) in [143, 144]:
            kw['created'] = E2011
            kw['updated'] = E2011
        c = data.add(models.Chapter, row['id'], **kw)
        c.area = data['Area'][row['area_id']]
    DBSession.flush()

    for row in old_db.execute("select * from feature"):
        kw = dict(id=row['id'], name=row['name'], ordinal_qualifier=row['id'][-1])
        if row['id'].startswith('143') or row['id'].startswith('144'):
            kw['created'] = E2011
            kw['updated'] = E2011
        param = data.add(models.Feature, row['id'], **kw)
        param.chapter = data['Chapter'][row['chapter_id']]
    DBSession.flush()

    for row in old_db.execute("select * from value"):
        desc = row['description']
        if desc == 'SOV & NegV/VNeg':
            if row['icon_id'] != 's9ff':
                desc += ' (a)'
            else:
                desc += ' (b)'

        data.add(
            common.DomainElement, (row['feature_id'], row['numeric']),
            id='%s-%s' % (row['feature_id'], row['numeric']),
            name=desc,
            description=row['long_description'],
            jsondata=dict(icon=Icons.id(row['icon_id'])),
            number=row['numeric'],
            parameter=data['Feature'][row['feature_id']])
    DBSession.flush()

    same = 0
    added = 0
    for row in old_db.execute("select * from datapoint"):
        parameter = data['Feature'][row['feature_id']]
        language = data['WalsLanguage'][row['language_id']]
        id_ = '%s-%s' % (parameter.id, language.id)
        created = E2008
        updated = E2008

        value_numeric = row['value_numeric']
        if (language.id, parameter.id) in vs2008:
            if vs2008[(language.id, parameter.id)] != row['value_numeric']:
                print '~~~', id_, vs2008[(language.id, parameter.id)], '-->', row['value_numeric']
                value_numeric = vs2008[(language.id, parameter.id)]
            else:
                same += 1
        else:
            updated = E2011
            created = E2011
            if parameter.id[-1] == 'A' and not (parameter.id.startswith('143') or parameter.id.startswith('144')):
                added += 1

        kw = dict(id=id_, updated=updated, created=created)
        valueset = data.add(
            common.ValueSet, row['id'],
            language=language,
            parameter=parameter,
            contribution=parameter.chapter,
            **kw)
        data.add(
            common.Value, row['id'],
            domainelement=data['DomainElement'][(row['feature_id'], value_numeric)],
            valueset=valueset,
            **kw)

    print same, 'datapoints did not change'
    print added, 'datapoints added to existing features'

    DBSession.flush()

    for row in old_db.execute("select * from datapoint_reference"):
        common.ValueSetReference(
            valueset=data['ValueSet'][row['datapoint_id']],
            source=data['Source'][row['reference_id']],
            description=row['note'],
        )

    for row in old_db.execute("select * from author_chapter"):
        DBSession.add(common.ContributionContributor(
            ord=row['order'],
            primary=row['primary'] != 0,
            contributor_pk=data['Contributor'][row['author_id']].pk,
            contribution_pk=data['Chapter'][row['chapter_id']].pk))

    lang.name = 'SPECIAL--' + lang.name


def prime_cache(args):
    """
    we use a versioned session to insert the changes in value assignment
    """
    #
    # compute the changes from 2008 to 2011:
    #
    vs2008 = get_vs2008(args)
    for row in DB.execute("select * from datapoint"):
        key = (row['language_id'], row['feature_id'])
        old_value = vs2008.get(key)
        new_value = row['value_numeric']
        if old_value and old_value != new_value:
            valueset = VersionedDBSession.query(common.ValueSet)\
                .join(common.Language)\
                .join(common.Parameter)\
                .filter(common.Parameter.id == row['feature_id'])\
                .filter(common.Language.id == row['language_id'])\
                .one()
            value = valueset.values[0]
            assert value.domainelement.number == old_value
            for de in valueset.parameter.domain:
                if de.number == new_value:
                    value.domainelement = de
                    break
            assert value.domainelement.number == new_value
            valueset.updated = E2011
            value.updated = E2011
            VersionedDBSession.flush()

    for row in rows(args.data_file('corrections_2013.tab'), namedtuples=True, newline='\r'):
        valueset = VersionedDBSession.query(common.ValueSet)\
            .join(common.Language)\
            .join(common.Parameter)\
            .filter(common.Parameter.id == row.feature)\
            .filter(common.Language.id == row.wals_code)\
            .one()
        value = valueset.values[0]

        if value.domainelement.number != int(row.old):
            print '--->', valueset.language.id, valueset.parameter.id, value.domainelement.number
        for de in valueset.parameter.domain:
            if de.number == int(row.new):
                value.domainelement = de
                break
        assert value.domainelement.number == int(row.new)
        valueset.updated = E2013
        value.updated = E2013
        VersionedDBSession.flush()

    # cache number of languages for a parameter:
    for parameter, valuesets in groupby(
            DBSession.query(common.ValueSet).order_by(common.ValueSet.parameter_pk),
            lambda vs: vs.parameter):
        representation = str(len(set(v.language_pk for v in valuesets)))

        d = None
        for _d in parameter.data:
            if _d.key == 'representation':
                d = _d
                break

        if d:
            d.value = representation
        else:
            d = common.Parameter_data(
                key='representation',
                value=representation,
                object_pk=parameter.pk)
            DBSession.add(d)

    compute_language_sources()


if __name__ == '__main__':
    initializedb(create=main, prime_cache=prime_cache)
