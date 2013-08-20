import codecs

from sqlalchemy.orm import joinedload_all
from path import path
from bs4 import BeautifulSoup as soup

from clld import RESOURCES
from clld.interfaces import IRepresentation
from clld.web.adapters import get_adapter
from clld.db.meta import DBSession
from clld.db.models.common import DomainElement, Contribution
from clld.web.util.helpers import button, icon, JS_CLLD
from clld.web.util.htmllib import HTML

import wals3
from wals3.models import Feature


def dataset_detail_html(context=None, request=None, **kw):
    return {
        'stats': context.get_stats(
            [rsc for rsc in RESOURCES if rsc.name
             in 'language contributor valueset'.split()]),
        'example_contribution': Contribution.get('1'),
        'citation': get_adapter(IRepresentation, context, request, ext='md.txt')}


def get_description(req, contribution):
    p = path(wals3.__file__).dirname().joinpath('static', 'descriptions', str(contribution.id), 'body.xhtml')
    c = codecs.open(p, encoding='utf8').read()

    adapter = get_adapter(IRepresentation, Feature(), req, ext='snippet.html')

    for feature in DBSession.query(Feature)\
        .filter(Feature.contribution_pk == contribution.pk)\
        .options(joinedload_all(Feature.domain, DomainElement.values)):
        table = soup(adapter.render(feature, req))
        values = '\n'.join(unicode(table.find(tag).extract()) for tag in ['thead', 'tbody'])
        c = c.replace('__values_%s__' % feature.id, values)

    return c.replace('http://wals.info', req.application_url)


def link_to_map(language):
    return HTML.a(
        icon('icon-globe'),
        title='show %s on map' % language.name,
        href="#map",
        onclick=JS_CLLD.mapShowInfoWindow(None, language.id))
