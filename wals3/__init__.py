from functools import partial

from sqlalchemy.orm import joinedload_all
from pyramid.config import Configurator
from pyramid.httpexceptions import HTTPNotFound

from clld.interfaces import IParameter, IMapMarker, IDomainElement, IMapMarker, IValue
from clld.web.adapters.base import Representation, adapter_factory
from clld.web.app import get_configurator, menu_item

from wals3.adapters import GeoJsonFeature
from wals3.maps import FeatureMap, FamilyMap, CountryMap, SampleMap
from wals3.datatables import Languages, Features, Datapoints
from wals3.models import Family, Country, WalsLanguage, Genus
from wals3.interfaces import IFamily, ICountry


def _(s, *args, **kw):
    return s

_('Contributions')
_('Contributors')
_('Sources')
_('Parameters')


def map_marker(ctx, req):
    de = None
    if IValue.providedBy(ctx):
        de = ctx.domainelement
    if IDomainElement.providedBy(ctx):
        de = ctx
    if de:
        return req.static_url('clld:web/static/icons/' + de.jsondata['icon'] + '.png')


def sample_factory(req):
    try:
        col = {
            '100': WalsLanguage.samples_100,
            '200': WalsLanguage.samples_200}[req.matchdict['count']]
    except KeyError:
        raise HTTPNotFound()

    class Sample(object):
        name = '%s-language sample' % req.matchdict['count']
        languages = req.db.query(WalsLanguage).filter(col == True)\
            .options(joinedload_all(WalsLanguage.genus, Genus.family))\
            .order_by(WalsLanguage.name)

    return Sample()


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    settings['sitemaps'] = 'contribution parameter source sentence valueset'.split()
    utilities = [
        #(ApicsCtxFactoryQuery(), interfaces.ICtxFactoryQuery),
        (map_marker, IMapMarker),
        #(frequency_marker, interfaces.IFrequencyMarker),
        #(link_attrs, interfaces.ILinkAttrs),
    ]
    config = get_configurator('wals3', *utilities, **dict(settings=settings))
    config.register_menu(
        ('dataset', partial(menu_item, 'dataset', label='Home')),
        ('parameters', partial(menu_item, 'parameters')),
        ('contributions', partial(menu_item, 'contributions')),
        ('languages', partial(menu_item, 'languages')),
        ('sources', partial(menu_item, 'sources')),
        ('contributors', partial(menu_item, 'contributors')),
        #newsblog
        #contact?
        #help?
    )
    #config.add_menu_item(
    #    'blog', lambda ctx, req: ('http://blog.wals.info/category/news/', 'Newsblog'))

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

    config.add_route('sample', '/languoid/samples/{count}', factory=sample_factory)
    config.register_map('sample', SampleMap)

    config.register_adapter(GeoJsonFeature, IParameter)
    config.add_route('feature_info', '/feature-info/{id}')
    config.add_route('genealogy', '/languoid/genealogy')
    return config.make_wsgi_app()
