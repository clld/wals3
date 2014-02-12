import codecs
from itertools import groupby

from sqlalchemy.orm import joinedload_all, joinedload
from path import path
from bs4 import BeautifulSoup as soup
from pyramid.httpexceptions import HTTPFound

from clld import RESOURCES
from clld.interfaces import IRepresentation
from clld.web.adapters import get_adapter
from clld.db.meta import DBSession
from clld.db.models.common import DomainElement, Contribution, ValueSet, Value
from clld.web.util.helpers import button, icon, JS_CLLD, get_referents, JS
from clld.web.util.multiselect import MultiSelect, CombinationMultiSelect
from clld.web.util.htmllib import HTML
from clld.web.icon import ICON_MAP

import wals3
from wals3.models import Feature, WalsLanguage, Genus
from wals3.maps import CombinedMap


def icons(req, param):
    icon_map = req.registry.settings['icons']
    td = lambda spec: HTML.td(
        HTML.img(
            src=req.static_url('clld:web/static/icons/' + icon_map[spec] + '.png'),
            height='20',
            width='20'),
        onclick='WALS3.reload({"%s": "%s"})' % (param, spec))
    rows = [
        HTML.tr(*map(td, icons)) for c, icons in
        groupby(sorted(icon_map.keys()), lambda spec: spec[0])]
    return HTML.div(
        HTML.table(
            HTML.tbody(*rows),
            class_="table table-condensed"
        ),
        button('Close', **{'data-dismiss': 'clickover'}))


class LanguoidSelect(MultiSelect):
    def format_result(self, l):
        return dict(
            id='%s-%s' % (l.mapper_name().lower()[0], l.id),
            text=l.name,
            type=l.mapper_name())

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

    p = path(wals3.__file__).dirname().joinpath('static', 'descriptions', str(context.id), 'body.xhtml')
    c = codecs.open(p, encoding='utf8').read()

    adapter = get_adapter(IRepresentation, Feature(), request, ext='snippet.html')

    for feature in DBSession.query(Feature)\
            .filter(Feature.contribution_pk == context.pk)\
            .options(joinedload_all(Feature.domain, DomainElement.values)):
        table = soup(adapter.render(feature, request))
        values = '\n'.join(unicode(table.find(tag).extract()) for tag in ['thead', 'tbody'])
        c = c.replace('__values_%s__' % feature.id, values)

    return {'text': c.replace('http://wals.info', request.application_url)}


def _valuesets(parameter):
    return DBSession.query(ValueSet)\
        .filter(ValueSet.parameter_pk == parameter.pk)\
        .options(
            joinedload(ValueSet.language),
            joinedload_all(ValueSet.values, Value.domainelement))


def parameter_detail_tab(context=None, request=None, **kw):
    query = _valuesets(context).options(joinedload_all(
        ValueSet.language, WalsLanguage.genus, Genus.family))
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
    """feature combination view
    """
    convert = lambda spec: ''.join(c if i == 0 else c + c for i, c in enumerate(spec))
    for i, de in enumerate(context.domain):
        param = 'v%s' % i
        if param in request.params:
            name = convert(request.params[param])
            if name in ICON_MAP:
                de.icon = ICON_MAP[name]

    return dict(
        select=CombinationMultiSelect(request, combination=context),
        map=CombinedMap(context, request))
