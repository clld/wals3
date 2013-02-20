import codecs

from sqlalchemy.orm import joinedload_all
from path import path
from bs4 import BeautifulSoup as soup

from clld.interfaces import IRepresentation, IIndex
from clld.web.adapters import get_adapter
from clld.db.meta import DBSession
from clld.db.models.common import DomainElement

import wals3
from wals3.models import Feature


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
