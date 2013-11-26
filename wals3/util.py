import codecs
from itertools import groupby, product

from sqlalchemy.orm import joinedload_all
from path import path
from bs4 import BeautifulSoup as soup
from pyramid.httpexceptions import HTTPFound

from clld import RESOURCES
from clld.interfaces import IRepresentation
from clld.web.adapters import get_adapter
from clld.db.meta import DBSession
from clld.db.models.common import DomainElement, Contribution, Parameter, Combination
from clld.web.util.helpers import button, icon, JS_CLLD, get_referents, JS
from clld.web.util.multiselect import MultiSelect
from clld.web.util.htmllib import HTML
from clld.web.icon import ICONS

import wals3
from wals3.models import Feature
from wals3.maps import CombinedMap


class CombinedDomainElement(object):
    def __init__(self, id_, name, *languages):
        self.id = id_
        self.strid = '-'.join(map(str, self.id))
        self.name = name
        self.icon_url = None
        self.languages = list(languages)


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


class ParameterMultiSelect(MultiSelect):
    def format_result(self, obj):
        return {'id': obj.id, 'text': '%s: %s' % (obj.id, obj.name)}

    def get_options(self):
        return {
            'data': [self.format_result(o) for o in self.collection],
            'multiple': True}


def _combine(context, request):
    if 'features' in request.params:
        id_ = Combination.delimiter.join(request.params['features'].split(','))
        if id_ != context.id or not isinstance(context, Combination):
            raise HTTPFound(request.route_url('combination', id=id_))


def parameter_detail_html(context=None, request=None, **kw):
    _combine(context, request)
    return dict(
        select=ParameterMultiSelect(
            request, 'features', 'features', collection=DBSession.query(Parameter).all()))


def combination_detail_html(context=None, request=None, **kw):
    """feature combination view
    """
    _combine(context, request)

    # cycle through colors per de number:
    pcolors = ['0000dd', '009900', '990099', 'dd0000', 'ffff00', 'ffffff', '00ff00', '00ffff', 'cccccc', 'ff6600']
    scolors = []
    shapes = ['c', 't', 'd', 's', 'f']

    icon_map = {}
    for icon_ in ICONS:
        icon_map[icon_.name] = icon_
        if icon_.name[1:] not in pcolors:
            scolors.append(icon_.name[1:])

    specs = list(product(shapes, pcolors)) + list(product(shapes, scolors))
    specs = [''.join(s) for s in specs]

    domain = {}
    for de in context.domain:
        id_ = tuple(d.number for d in de)
        domain[id_] = CombinedDomainElement(id_, ' / '.join(d.name for d in de))

    for language, values in groupby(
        # group values by language
        sorted(context.values, key=lambda v: v.valueset.language_pk),
        lambda i: i.valueset.language
    ):
        vs = {v.valueset.parameter_pk: v.domainelement.number for v in values}
        domain[tuple(vs[p.pk] for p in context.parameters)].languages.append(language)

    convert = lambda spec: ''.join(c if i == 0 else c + c for i, c in enumerate(spec))

    for i, de in enumerate(sorted(domain.keys())):
        de = domain[de]
        param = 'v%s' % i
        if param in request.params:
            spec = convert(request.params[param])
        else:
            spec = specs[i % len(specs)]
        de.icon_url = icon_map[spec].url(request)

    return dict(
        select=ParameterMultiSelect(
            request, 'features', 'features', collection=DBSession.query(Parameter).all()),
        map=CombinedMap(domain, request),
        domain=domain)


def partitioned(items, n=3):
    max_items_per_bucket, rem = divmod(len(items), n)
    if rem:
        max_items_per_bucket += 1
    bucket = []

    for item in items:
        if len(bucket) >= max_items_per_bucket:
            yield bucket
            bucket = []
        bucket.append(item)

    yield bucket


def link_to_map(language):
    return HTML.a(
        icon('icon-globe'),
        title='show %s on map' % language.name,
        href="#map",
        onclick=JS_CLLD.mapShowInfoWindow(None, language.id))
