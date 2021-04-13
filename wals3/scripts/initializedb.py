import re
import json
import collections
import datetime

from bs4 import BeautifulSoup
from tqdm import tqdm

import transaction
import pycldf

from clld.cliutil import Data, slug, bibtex2source, add_language_codes
from clld.db.meta import DBSession
from clld.db.models import common
from clld.lib.bibtex import Database

import wals3
from wals3 import models


def main(args):  # pragma: no cover

    repos = args.cldf.directory.parent
    cldf_dir = repos / 'cldf'
    args.log.info('Loading dataset')
    ds = list(pycldf.iter_datasets(cldf_dir))[0]
    data = Data()

    dataset = common.Dataset(
        id='wals',
        name='WALS Online',
        description=ds.properties['dc:title'],
        published=datetime.date(2013, 8, 15),
        publisher_name="Max Planck Institute for Evolutionary Anthropology",
        publisher_place="Leipzig",
        publisher_url="https://www.eva.mpg.de",
        license=ds.properties['dc:license'],
        contact='wals@shh.mpg.de',
        jsondata={
            'license_icon': 'cc-by.png',
            'license_name':
                'Creative Commons Attribution 4.0 International License',
        },
        domain=ds.properties['dc:identifier'].split('://')[1])

    DBSession.add(dataset)
    DBSession.flush()

    for rec in tqdm(Database.from_file(ds.bibpath), desc='Processing sources'):
        jsondata = collections.defaultdict(dict)
        ns = bibtex2source(rec, common.Source)
        # preserve original names and ids
        if 'wals_ref_name' in rec and rec['wals_ref_name']:
            ns.name = rec['wals_ref_name']
        ns.id = rec.id
        try:
            if rec['google_book_search_id']:
                ns.google_book_search_id = rec['google_book_search_id']
                jsondata['gbs']['volumeInfo'] = {
                    'industryIdentifiers': [{'identifier': ns.google_book_search_id, 'type': ''}]
                }
                jsondata['gbs']['accessInfo'] = {'viewability': rec['google_book_viewability']}
        except KeyError:
            pass
        for k in ['iso_code', 'wals_code', 'olac_field']:
            if k in rec and rec[k]:
                jsondata[k] = list(map(lambda x: x.strip(), rec[k].split(';')))
        ns.jsondata = jsondata
        data.add(common.Source, ns.id, _obj=ns)
    DBSession.flush()

    for row in ds.iter_rows('areas.csv'):
        data.add(models.Area, row['ID'],
                 id=row['ID'],
                 name=row['Name'],
                 dbpedia_url=row['dbpedia_url'])
    DBSession.flush()

    for row in ds.iter_rows('countries.csv'):
        data.add(models.Country, row['ID'],
                 id=row['ID'],
                 name=row['Name'])
    DBSession.flush()

    for row in ds.iter_rows('contributors.csv'):
        c = data.add(common.Contributor, row['ID'],
                     id=row['ID'],
                     name=row['Name'],
                     url=row['Url'])
        if row['Editor_Ord']:
            data.add(common.Editor, row['Editor_Ord'],
                     dataset=dataset,
                     contributor=c,
                     ord=row['Editor_Ord'])
    DBSession.flush()

    for row in ds.iter_rows('chapters.csv'):
        desc, area_pk = None, None
        descr_path = cldf_dir / ds.get_row_url('chapters.csv', row)
        if descr_path.exists():
            desc = open(descr_path).read()
        if row['Area_ID'] in data['Area']:
            area_pk = data['Area'][row['Area_ID']].pk
        c = data.add(models.Chapter, row['ID'],
                     id=row['ID'],
                     name=row['Name'],
                     description=desc,
                     sortkey=row['Number'],
                     wp_slug=row['wp_slug'],
                     area_pk=area_pk)
        if row['Source']:
            for s in row['Source']:
                data.add(common.ContributionReference, s,
                         contribution=c,
                         source_pk=data['Source'][s].pk)
        cnt = 0
        for i, f in enumerate(['Contributor_ID', 'With_Contributor_ID']):
            if row[f]:
                for co in row[f]:
                    data.add(common.ContributionContributor, co,
                             contribution=c,
                             contributor_pk=data['Contributor'][co].pk,
                             primary=(i == 0),
                             ord=cnt)
                    cnt += 1
    DBSession.flush()

    feat2chapter = {}
    for row in ds.iter_rows('ParameterTable'):
        feat2chapter[row['ID']] = row['Chapter_ID']
        data.add(models.Feature, row['ID'],
                 id=row['ID'],
                 name=row['Name'],
                 contribution_pk=data['Chapter'][row['Chapter_ID']].pk,
                 representation=0,
                 ordinal_qualifier=row['ID'].replace(row['Chapter_ID'], ''))
    DBSession.flush()

    glossary_file = cldf_dir / 'docs' / 'chapter_s2.html'
    parsed = BeautifulSoup(glossary_file.read_text(), 'html.parser')
    for abbr, desc in zip(parsed.find_all('dt'), parsed.find_all('dd')):
        # ID has dots -> add directly
        new = common.GlossAbbreviation(
            id=abbr.contents[0],
            name=desc.contents[0])
        data['GlossAbbreviation'][abbr.contents[0]] = new
        DBSession.add(new)
    DBSession.flush()

    lrefs = collections.defaultdict(list)
    gl_value = common.IdentifierType.get('glottolog').value
    for row in tqdm(ds.iter_rows('LanguageTable'), desc='Processing languages'):
        fam, gen = None, None
        if row['Family']:
            try:
                fam = data['Family'][slug(row['Family'])]
            except KeyError:
                fam = data.add(models.Family, slug(row['Family']), id=slug(row['Family']), name=row['Family'])
            if row['Genus']:
                try:
                    gen = data['Genus'][slug(row['Genus'])]
                except KeyError:
                    gen = data.add(models.Genus, slug(row['Genus']),
                                   id=slug(row['Genus']),
                                   name=row['Genus'],
                                   subfamily=row['Subfamily'],
                                   icon=row['GenusIcon'],
                                   family=fam)
        if fam is None and gen is None:  # Isolate
            n = slug(row['Name'])
            try:
                fam = data['Family'][n]
            except KeyError:
                fam = data.add(models.Family, n, id=n, name=row['Name'])
            try:
                gen = data['Genus'][n]
            except KeyError:
                gen = data.add(models.Genus, n,
                               id=n,
                               name=row['Name'],
                               icon=row['GenusIcon'],
                               family=fam)
        d = data.add(models.WalsLanguage, row['ID'],
                     id=row['ID'],
                     name=row['Name'],
                     ascii_name=slug(row['Name'], remove_whitespace=False),
                     latitude=row['Latitude'],
                     longitude=row['Longitude'],
                     macroarea=row['Macroarea'],
                     iso_codes=', '.join(row['ISO_codes']),
                     samples_100=row['Samples_100'],
                     samples_200=row['Samples_200'],
                     genus=gen)
        DBSession.flush()
        if row['Country_ID']:
            for c in row['Country_ID']:
                data.add(models.CountryLanguage, c, country_pk=data['Country'][c].pk, language_pk=d.pk)
        # first iso codes then glottocodes to avoid having glottocode duplicates in db
        # an iso triggers adding of the corresponding glottocode if any
        if row['ISO_codes']:
            for iso in row['ISO_codes']:
                add_language_codes(data, d, isocode=iso)
        if row['Glottocode'] and '{}:{}'.format(
                gl_value, row['Glottocode']) not in data['Identifier']:
            add_language_codes(data, d, isocode=None, glottocode=row['Glottocode'])
        if row['Source']:
            lpk = data['WalsLanguage'][row['ID']].pk
            for s in row['Source']:
                if s not in lrefs[lpk]:
                    lrefs[lpk].append(data['Source'][s].pk)
    DBSession.flush()

    for row in tqdm(ds.iter_rows('language_names.csv'), desc='Processing language names'):
        i = data.add(common.Identifier, row['ID'],
                     id='{}:{}'.format(slug(row['Provider']), slug(row['Name'])),
                     name=row['Name'],
                     description=row['Provider'],
                     type='name')
        for lg_id in row['Language_ID']:
            DBSession.add(
                common.LanguageIdentifier(language=data['WalsLanguage'][lg_id], identifier=i))
    DBSession.flush()

    for row in ds.iter_rows('CodeTable'):
        data.add(common.DomainElement, row['ID'],
                 id=row['ID'],
                 name=row['Name'],
                 description=row['Description'],
                 number=row['Number'],
                 jsondata={'icon': row['icon']},
                 parameter_pk=data['Feature'][row['Parameter_ID']].pk)
    DBSession.flush()

    for row in ds.iter_rows('ExampleTable'):
        data.add(common.Sentence, row['ID'],
                 id=row['ID'],
                 name=row['Primary_Text'],
                 description=row['Translated_Text'],
                 analyzed='\t'.join(row['Analyzed_Word']),
                 gloss='\t'.join(row['Gloss']),
                 language_pk=data['WalsLanguage'][row['Language_ID']].pk)
    DBSession.flush()

    srcdescr = re.compile(r'^(.*?)\[(.*?)\]$')
    flush_cnt = 0
    for row in tqdm(ds.iter_rows('ValueTable'), desc='Processing values'):
        lpk = data['WalsLanguage'][row['Language_ID']].pk
        vs = data.add(common.ValueSet, row['ID'],
                      id=row['ID'],
                      language_pk=lpk,
                      parameter_pk=data['Feature'][row['Parameter_ID']].pk,
                      contribution_pk=data['Chapter'][feat2chapter[row['Parameter_ID']]].pk)
        if row['Source']:
            for s in row['Source']:
                try:
                    s_, descr = srcdescr.search(s).groups()
                except AttributeError:
                    s_ = s
                    descr = ''
                spk = data['Source'][s_].pk
                data.add(common.ValueSetReference, s_,
                         valueset=vs,
                         description=descr,
                         source_pk=spk)
                if spk not in lrefs[lpk]:
                    lrefs[lpk].append(spk)
        v = data.add(common.Value, row['ID'],
                     id=row['ID'],
                     valueset=vs,
                     description=row['Comment'],
                     domainelement_pk=data['DomainElement'][row['Code_ID']].pk)
        if row['Example_ID']:
            for e in row['Example_ID']:
                data.add(common.ValueSentence, e,
                         value=v,
                         sentence_pk=data['Sentence'][e].pk)
        if not flush_cnt % 1000:
            DBSession.flush()
        flush_cnt += 1

    for lpk, spks in lrefs.items():
        for spk in spks:
            data.add(common.LanguageSource, lpk,
                     language_pk=lpk,
                     source_pk=spk)
    DBSession.flush()


def prime_cache(args):
    # add number of data points per parameter
    for feat in DBSession.query(models.Feature):
        q = DBSession.query(common.ValueSet.language_pk)\
            .filter(common.ValueSet.parameter_pk == feat.pk)\
            .distinct()
        feat.representation = q.count()
