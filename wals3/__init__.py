from pyramid.config import Configurator
from sqlalchemy import engine_from_config, desc
from sqlalchemy.orm import joinedload
from mako.template import Template
from markupsafe import Markup

from clld import interfaces
from clld.web import datatables
from clld.web.datatables.base import Col
from clld.web.adapters import GeoJson

from wals3.models import WalsLanguage, Genus, Family
from wals3.adapters import GeoJsonFeature
from wals3.maps import FeatureMap


def _(s, *args, **kw):
    return s

_('Languages')


class GenusCol(Col):
    def order(self, direction):
        return desc(Genus.name) if direction == 'desc' else Genus.name

    def search(self, qs):
        return Genus.name.contains(qs)

    def format(self, item):
        return item.genus.name


class Languages(datatables.Languages):
    def base_query(self, query):
        return query.join(Genus).join(Family).options(joinedload(WalsLanguage.genus))

    def col_defs(self):
        cols = datatables.Languages.col_defs(self)
        return cols[:2] + [GenusCol(self, 'genus')] + cols[2:]


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
    config.scan()
    return config.make_wsgi_app()
