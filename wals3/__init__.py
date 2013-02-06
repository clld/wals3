from functools import partial
import re

from path import path
from pyramid.config import Configurator

from clld.interfaces import IParameter
from clld.web.adapters import GeoJson, Representation

import wals3
from wals3.adapters import GeoJsonFeature
from wals3.maps import FeatureMap, FamilyMap
from wals3.datatables import Languages, Features
from wals3 import views
from wals3.models import Family
from wals3.interfaces import IFamily


def _(s, *args, **kw):
    return s

_('Languages')


ADAPTER_COUNTER = 0


def adapter_factory(template, mimetype='text/html', extension='html', base=None):
    global ADAPTER_COUNTER
    base = base or Representation
    extra = dict(mimetype=mimetype, extension=extension, template=template)
    cls = type('WALSRenderer%s' % ADAPTER_COUNTER, (base,), extra)
    ADAPTER_COUNTER += 1
    return cls


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    settings['mako.directories'] = ['wals3:templates', 'clld:web/templates']
    settings['clld.app_template'] = "wals3.mako"

    config = Configurator(settings=settings)
    config.include('clld.web.app')
    config.register_app('wals3')

    config.register_datatable('languages', Languages)
    config.register_datatable('parameters', Features)
    config.register_map('parameter', FeatureMap)

    config.register_resource('family', Family, IFamily)
    config.register_adapter(adapter_factory('family/detail_html.mako'), IFamily)
    config.register_map('family', FamilyMap)

    config.override_asset(
        to_override='clld:web/templates/language/rdf.pt',
        override_with='wals3:templates/language/rdf.pt')

    config.register_adapter(GeoJsonFeature, IParameter)

    return config.make_wsgi_app()
