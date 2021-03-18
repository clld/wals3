"""

"""
import re
import json
import pathlib
import contextlib
import collections

import transaction
from clldutils import db
from clldutils import clilib
from clldutils.misc import data_url
from clld.db.meta import DBSession
from clld.db.models import common
from clld.lib.bibtex import EntryType
from csvw.dsv import reader

import wals3
from wals3 import models

# FIXME:
# - source.bib - we should import source data from the bib file, because this can be easier
#   maintained.


def typed(r, t):  # pragma: no cover
    if 'version' in r:
        del r['version']
    for k in r:
        if k.endswith('_pk') or k == 'pk' or k.endswith('_int'):
            r[k] = int(r[k]) if r[k] != '' else None
        elif k == 'jsondata':
            r[k] = json.loads(r[k]) if r[k] else None
        elif k in {'latitude', 'longitude'}:
            r[k] = float(r[k]) if r[k] != '' else None
        elif k in {'samples_100', 'samples_200'}:
            r[k] = r[k] == 't'

    if t in {'editor.csv', 'contributioncontributor.csv'}:
        r['primary'] = r['primary'] == 't'
        r['ord'] = int(r['ord'])
    elif t == 'contribution.csv':
        r['sortkey'] = int(r['sortkey'])
        r['date'] = None
    elif t == 'parameter.csv':
        r['blog_title'] = None
    elif t == 'value.csv':
        r['frequency'] = None
    elif t == 'source.csv':
        r['bibtex_type'] = r['bibtex_type'] or 'misc'
        r['bibtex_type'] = EntryType.get(r['bibtex_type'])
    return r


def main(args):  # pragma: no cover

    repos = args.cldf.directory.parent

    def iterrows(core, extended=False):
        res = collections.OrderedDict()
        for row in reader(repos / 'raw' / core, dicts=True):
            res[row['pk']] = row
        if extended:
            for row in reader(repos / 'raw' / extended, dicts=True):
                res[row['pk']].update(row)
        for r in res.values():
            yield typed(r, core)

    desc_dir = repos / 'raw' / 'descriptions'
    src_pattern = re.compile(
        'src="https?://wals.info/static/descriptions/(?P<sid>s?[0-9]+)/images/(?P<fname>[^"]+)"')

    def repl(m):
        p = desc_dir.joinpath(m.group('sid'), 'images', m.group('fname'))
        if p.exists():
            return 'src="{0}"'.format(data_url(p))
        return m.string[m.start():m.end()]

    descs = {}
    for d in desc_dir.iterdir():
        if d.is_dir():
            descs[d.stem] = src_pattern.sub(
                repl, d.joinpath('body.xhtml').read_text(encoding='utf8'))

    for stem, cls in [
        ('dataset', common.Dataset),
        ('contributor', common.Contributor),
        ('editor', common.Editor),
        ('glossabbreviation', common.GlossAbbreviation),
        ('country', models.Country),
        ('area', models.Area),
    ]:
        for row in iterrows(stem + '.csv'):
            DBSession.add(cls(**row))
        DBSession.flush()

    for row in iterrows('contribution.csv', extended='chapter.csv'):
        row['description'] = descs.get(row['id'])
        DBSession.add(models.Chapter(**row))
        DBSession.flush()

    for stem, cls in [
        ('contributioncontributor', common.ContributionContributor),
        ('family', models.Family),
        ('genus', models.Genus),
        ('identifier', common.Identifier),
    ]:
        for row in iterrows(stem + '.csv'):
            DBSession.add(cls(**row))
        DBSession.flush()

    for row in iterrows('language.csv', extended='walslanguage.csv'):
        DBSession.add(models.WalsLanguage(**row))
        DBSession.flush()

    for row in iterrows('parameter.csv', extended='feature.csv'):
        DBSession.add(models.Feature(**row))
        DBSession.flush()

    for stem, cls in [
        ('languageidentifier', common.LanguageIdentifier),
        ('countrylanguage', models.CountryLanguage),
        ('domainelement', common.DomainElement),
        ('valueset', common.ValueSet),
        ('value', common.Value),
        ('sentence', common.Sentence),
        ('valuesentence', common.ValueSentence),
        ('source', common.Source),
        ('languagesource', common.LanguageSource),
        ('valuesetreference', common.ValueSetReference),
        ('contributionreference', common.ContributionReference),
        ('config', common.Config),
    ]:
        for row in iterrows(stem + '.csv'):
            DBSession.add(cls(**row))
        DBSession.flush()
