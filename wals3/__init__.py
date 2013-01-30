from pyramid.config import Configurator

from clld import interfaces
from clld.web.adapters import GeoJson

from wals3.adapters import GeoJsonFeature
from wals3.maps import FeatureMap
from wals3.datatables import Languages, Features
from wals3 import views


def _(s, *args, **kw):
    return s

_('Languages')


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    settings['mako.directories'] = ['wals3:templates', 'clld:web/templates']
    settings['clld.app_template'] = "wals3.mako"

    config = Configurator(settings=settings)

    #
    # must add project specific translation dir first
    #
    config.add_translation_dirs('wals3:locale')

    #
    # then include clld, thereby adding the default translations
    #
    config.include('clld.web.app')

    config.register_datatable('languages', Languages)
    config.register_datatable('parameters', Features)
    config.register_map('parameter', FeatureMap)

    config.override_asset(
        to_override='clld:web/templates/language/rdf.pt',
        override_with='wals3:templates/language/rdf.pt')

    config.register_adapter(
        GeoJsonFeature,
        interfaces.IParameter,
        interfaces.IRepresentation,
        GeoJson.mimetype)

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.scan(views)
    return config.make_wsgi_app()
