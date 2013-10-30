import codecs

from sqlalchemy.orm import joinedload_all
from path import path
from bs4 import BeautifulSoup as soup
from pyramid.httpexceptions import HTTPFound

from clld import RESOURCES
from clld.interfaces import IRepresentation
from clld.web.adapters import get_adapter
from clld.db.meta import DBSession
from clld.db.models.common import DomainElement, Contribution
from clld.web.util.helpers import button, icon, JS_CLLD, get_referents, JS
from clld.web.util.multiselect import MultiSelect
from clld.web.util.htmllib import HTML

import wals3
from wals3.models import Feature


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


def link_to_map(language):
    return HTML.a(
        icon('icon-globe'),
        title='show %s on map' % language.name,
        href="#map",
        onclick=JS_CLLD.mapShowInfoWindow(None, language.id))
