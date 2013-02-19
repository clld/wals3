from functools import partial
import re

from path import path
from pyramid.config import Configurator

from clld.interfaces import IParameter
from clld.web.adapters import GeoJson, Representation

import wals3
from wals3.adapters import GeoJsonFeature
from wals3.maps import FeatureMap, FamilyMap, CountryMap
from wals3.datatables import Languages, Features, Datapoints
from wals3 import views
from wals3.models import Family, Country
from wals3.interfaces import IFamily, ICountry


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
    settings['clld.menuitems_list'] = 'parameters contributions languages sources contributors'.split()

    config = Configurator(settings=settings)
    config.include('clld.web.app')
    config.register_app('wals3')

    config.add_menu_item('blog', lambda ctx, req: ('http://blog.wals.info/category/news/', 'Newsblog'))

    config.register_datatable('values', Datapoints)
    config.register_datatable('languages', Languages)
    config.register_datatable('parameters', Features)
    config.register_map('parameter', FeatureMap)

    config.register_resource('family', Family, IFamily)
    config.register_adapter(adapter_factory('family/detail_html.mako'), IFamily)
    config.register_map('family', FamilyMap)

    config.register_resource('country', Country, ICountry)
    config.register_adapter(adapter_factory('country/detail_html.mako'), ICountry)
    config.register_map('country', CountryMap)

    config.override_asset(
        to_override='clld:web/templates/language/rdf.pt',
        override_with='wals3:templates/language/rdf.pt')

    config.register_adapter(GeoJsonFeature, IParameter)
    config.add_route('feature_info', '/feature-info/{id}')
    config.add_route('genealogy', '/languoid/genealogy')
    return config.make_wsgi_app()
