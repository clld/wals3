import re

from sqlalchemy import func
from sqlalchemy.orm import joinedload
from bs4 import BeautifulSoup as soup
from pyramid.httpexceptions import HTTPFound

from clld import RESOURCES
from clld.interfaces import IRepresentation
from clld.web.adapters import get_adapter
from clld.db.meta import DBSession
from clld.db.models.common import Contribution, ValueSet, Value
from clld.web.util.helpers import get_referents, JS
from clld.web.util.multiselect import MultiSelect, CombinationMultiSelect
from clld.web.icon import ICON_MAP

import wals3
from wals3.models import Feature, WalsLanguage, Genus


class LanguoidSelect(MultiSelect):

    """Allow selection of languoids by name.

    >>> ls = LanguoidSelect(None, None, None)
    >>> assert ls.get_options()
    """

    def format_result(self, l):
        return dict(
            id='%s-%s' % (l.__class__.__name__.lower()[0], l.id),
            text=l.name,
            type=l.__class__.__name__)

    def get_options(self):
        return {
            'multiple': False,
            'placeholder': 'Search a languoid by name',
            'formatResult': JS('WALS3.formatLanguoid'),
            'formatSelection': JS('WALS3.formatLanguoid')}


def language_index_html(context=None, request=None, **kw):
    return {'ms': LanguoidSelect(
        request, 'languoid', 'languoid', url=request.route_url('languoids'))}


def dataset_detail_html(context=None, request=None, **kw):
    return {
        'stats': context.get_stats(
            [rsc for rsc in RESOURCES if rsc.name
             in 'language contributor valueset'.split()]),
        'example_contribution': Contribution.get('1'),
        'citation': get_adapter(IRepresentation, context, request, ext='md.txt')}


def source_detail_html(context=None, request=None, **kw):
    return {'referents': get_referents(context)}


def contribution_detail_html(context=None, request=None, **kw):
    if context.id == 's4':
        raise HTTPFound(request.route_url('genealogy'))

    c = context.description
    if '<body>' in c:
        c = c.split('<body>')[1].split('</body>')[0]
    adapter = get_adapter(IRepresentation, Feature(), request, ext='snippet.html')
    fids = [m.group('fid') for m in re.finditer('__values_(?P<fid>[0-9A-Z]+)__', c)]

    for feature in DBSession.query(Feature)\
            .filter(Feature.id.in_(fids))\
            .options(joinedload(Feature.domain)):
        counts = DBSession.query(Value.domainelement_pk, func.count(Value.pk))\
            .filter(Value.domainelement_pk.in_([de.pk for de in feature.domain]))\
            .group_by(Value.domainelement_pk)
        feature.counts = dict(counts)
        table = soup(adapter.render(feature, request), features='html5lib')
        values = '\n'.join('%s' % table.find(tag).extract() for tag in ['thead', 'tbody'])
        c = c.replace('__values_%s__' % feature.id, values)

    return {'text': c.replace('http://wals.info', request.application_url)}


def _valuesets(parameter):
    return DBSession.query(ValueSet)\
        .filter(ValueSet.parameter_pk == parameter.pk)\
        .options(
            joinedload(ValueSet.language),
            joinedload(ValueSet.values).joinedload(Value.domainelement))


def parameter_detail_tab(context=None, request=None, **kw):
    query = _valuesets(context).options(
        joinedload(ValueSet.language).joinedload(WalsLanguage.genus).joinedload(Genus.family))
    return dict(datapoints=query)


def parameter_detail_georss(context=None, request=None, **kw):
    return dict(datapoints=_valuesets(context))


def parameter_detail_xml(context=None, request=None, **kw):
    return dict(datapoints=_valuesets(context))


def parameter_detail_kml(context=None, request=None, **kw):
    return dict(datapoints=_valuesets(context))


def parameter_detail_html(context=None, request=None, **kw):
    return dict(select=CombinationMultiSelect(request, selected=[context]))


def combination_detail_html(context=None, request=None, **kw):
    """feature combination view."""
    convert = lambda spec: ''.join(c if i == 0 else c + c for i, c in enumerate(spec))
    for i, de in enumerate(context.domain):
        param = 'v%s' % i
        if param in request.params:
            name = convert(request.params[param])
            if name in ICON_MAP:
                de.icon = ICON_MAP[name]

    return dict(iconselect=True)
