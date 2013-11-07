from functools import partial
from string import ascii_uppercase
import re

from path import path
from sqlalchemy.orm import joinedload_all
from pyramid.httpexceptions import HTTPNotFound, HTTPMovedPermanently

from clld.interfaces import (
    IParameter, IMapMarker, IDomainElement, IValue, ILanguage,
    ICtxFactoryQuery, IBlog,
)
from clld.web.adapters.base import adapter_factory
from clld.web.app import get_configurator, menu_item, CtxFactoryQuery
from clld.db.models.common import Contribution, ContributionReference, Parameter

from wals3.blog import Blog
from wals3.adapters import GeoJsonFeature
from wals3.models import Family, Country, WalsLanguage, Genus
from wals3.interfaces import IFamily, ICountry, IGenus


_ = lambda s: s
_('Contributions')
_('Contributors')
_('Sources')
_('Parameters')
_('Parameter')
_('ValueSets')
_('Sentences')


def map_marker(ctx, req):
    """to allow for user-selectable markers, we have to look up a possible custom
    selection from the url params.
    """
    icon_map = req.registry.settings['icons']
    icon = None
    if IValue.providedBy(ctx):
        if 'v%s' % ctx.domainelement.number in req.params:
            icon = icon_map.get(req.params['v%s' % ctx.domainelement.number])
        else:
            icon = ctx.domainelement.jsondata['icon']
    elif IDomainElement.providedBy(ctx):
        if 'v%s' % ctx.number in req.params:
            icon = icon_map.get(req.params['v%s' % ctx.number])
        else:
            icon = ctx.jsondata['icon']
    elif ILanguage.providedBy(ctx):
        if ctx.genus.id in req.params:
            icon = icon_map.get(req.params[ctx.genus.id])
        else:
            icon = ctx.genus.icon
    elif isinstance(ctx, Genus):
        if ctx.id in req.params:
            icon = icon_map.get(req.params[ctx.id])
        else:
            icon = ctx.icon
    if icon:
        return req.static_url('clld:web/static/icons/' + icon + '.png')


class WalsCtxFactoryQuery(CtxFactoryQuery):
    def refined_query(self, query, model, req):
        """Derived classes may override this method to add model-specific query
        refinements of their own.
        """
        if model == Contribution:
            return query.options(joinedload_all(
                Contribution.references, ContributionReference.source))
        if model == Parameter:
            if req.matchdict['id'][-1] not in ascii_uppercase:
                # route match for 2008-style URL: redirect!
                raise HTTPMovedPermanently(
                    req.route_url('contribution', id=req.matchdict['id']))
        return query


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


#def legacy():
#    Route('root.unapi',                 '/unapi'),
#    Route('root.metadata',              '/metadata'),
#    Route('root.metadata.alt',          '/metadata.{extension}'),
#
#    Route('export',                     "/export", controller='root', action='export'),
#    Route('export.do',                  "/do_export", controller='root', action='do_export'),
#
#    Redirect("/feature",                "/feature/"),
#    Redirect("/feature",                "/feature/item{url:.*}", code=301),
#
#    #
#    # redirect legacy urls:
#    #
#    Redirect("/feature/{fid}A.tab", "/feature/tab/{fid:[0-9]+}", code=301),
#
#    Route('feature.combined.query',     "/feature/combined/{id1}", requirements=dict(id1=FEATURE_ID_PATTERN)),
#    Route('feature.combined',           "/feature/combined/{id1}/{id2}", requirements=dict(id1=FEATURE_ID_PATTERN, id2=FEATURE_ID_PATTERN)),
#    Route('feature.combined.alt',       "/feature/combined/{id1}/{id2}.{extension}", requirements=dict(id1=FEATURE_ID_PATTERN, id2=FEATURE_ID_PATTERN)),
#
#    Route('feature.metadata',           "/feature/metadata/{id}", requirements={"id": FEATURE_ID_PATTERN}),
#    Route('feature.metadata.alt',       "/feature/metadata/{id}.{extension}", requirements={"id": FEATURE_ID_PATTERN}),
#
#    Route('feature.search',             "/feature/search"),
#
#
#    Route('refdb.index.alt',            '/refdb/.{extension}'),
#    Route('refdb.unapi',                '/refdb/unapi'),
#
#
#    Route('refdb.records_by_iso_code',  '/refdb/records/'+ISO_CODE_PREFIX+'{id}', requirements=dict(id=R"[a-z]{3}")),
#    Route('refdb.records_by_iso_code.alt','/refdb/records/'+ISO_CODE_PREFIX+'{id}.{extension}', requirements=dict(id=R"[a-z]{3}")),
#
#    Route('refdb.records_by_wals_code', '/refdb/records/'+WALS_CODE_PREFIX+'{id}', requirements=dict(id=R"[a-z]{2,3}")),
#    Route('refdb.records_by_wals_code.alt','/refdb/records/'+WALS_CODE_PREFIX+'{id}.{extension}', requirements=dict(id=R"[a-z]{2,3}")),
#
#    Route('refdb.records_by_resource',  '/refdb/records/{id}', requirements=dict(id=R"[a-z0-9\-A-Z]+")),
#    Route('refdb.records_by_resource.alt','/refdb/records/{id}.{extension}', requirements=dict(id=R"[a-z0-9\-A-Z]+")),
#
#    Route('refdb.search.alt',           "/refdb/search_{what}", requirements=dict(what='author|title|language|journal')),
#
#    Route('refdb.metadata.alt',         "/refdb/metadata/{id}.{extension}", requirements={"id": R"(\d{1,4}|[\d\w\-]+)"}),
#
#    Route('languoid.metadata',          "/languoid/metadata/"+WALS_CODE_PREFIX+"{id}", requirements=dict(id=LECT_ID_PATTERN)),
#    Route('languoid.metadata.alt',      "/languoid/metadata/"+WALS_CODE_PREFIX+"{id}.{extension}", requirements=dict(id=LECT_ID_PATTERN)),
#    Route('languoid.unapi',             '/languoid/unapi'),
#    Route('languoid.by_name',           '/languoid/by_name'),
#    Route('languoid.by_code.query',     '/languoid/by_code'),
#    Route('languoid.by_code',           '/languoid/by_code/'+ISO_CODE_PREFIX+'{id}', requirements=dict(id=R"[a-z]{3}")),
#    Route('languoid.by_code.alt',       '/languoid/by_code/'+ISO_CODE_PREFIX+'{id}.{extension}', requirements=dict(id=R"[a-z]{3}")),
#    Route('languoid.by_geography',      '/languoid/by_geography'),
#
#    Route('languoid.genus.default',     "/languoid/genus/{id}", requirements=dict(id=R"[a-z]+")),
#    Route('languoid.genus.default.alt', "/languoid/genus/{id}.{extension}", requirements=dict(id=R"[a-z]+")),
#    Route('languoid.search',            "/languoid/search"),
#    Route('languoid.lects',             "/languoid/lects"),
#
#    Route('chapter.unapi',              "/chapter/unapi"),
#    Route('register.unapi',             "/register/unapi", controller='chapter'),
#    Route('chapter.metadata',           "/chapter/metadata/{id}", requirements={"id": CHAPTER_ID_PATTERN}),
#    Route('chapter.metadata.alt',       "/chapter/metadata/{id}.{extension}", requirements={"id": CHAPTER_ID_PATTERN}),
#
#    Route('supplement.default',         "/supplement/{id}", requirements={"id": SUPPLEMENT_ID_PATTERN}),
#    Route('supplement.default.alt',     "/supplement/{id}.{extension}", requirements={"id": SUPPLEMENT_ID_PATTERN}),
#    Route('supplement.metadata',        "/supplement/metadata/{id}", requirements={"id": SUPPLEMENT_ID_PATTERN}),
#    Route('supplement.metadata.alt',    "/supplement/metadata/{id}.{extension}", requirements={"id": SUPPLEMENT_ID_PATTERN}),
#    Route('supplement.unapi',           "/supplement/unapi"),
#
#    Route('datapoint.combined',         "/datapoint/{feature_id}/"+WALS_CODE_PREFIX+"{lect_id}", requirements=dict(lect_id=LECT_ID_PATTERN, feature_id=COMBINED_FEATURE_ID_PATTERN), action='default'),
#    Route('datapoint.comment',          "/datapoint/comment"),
#
#    Route('example.index',              "/example/{feature_id}/"+WALS_CODE_PREFIX+"{lect_id}", requirements=dict(lect_id=LECT_ID_PATTERN, feature_id=FEATURE_ID_PATTERN+"|all")),
#    Route('example.index.alt',          "/example/{feature_id}/"+WALS_CODE_PREFIX+"{lect_id}.{extension}", requirements=dict(lect_id=LECT_ID_PATTERN, feature_id=FEATURE_ID_PATTERN+"|all")),
#    Route('example.index.all_lects',    "/example/{feature_id}/{lect_id:all}", requirements=dict(feature_id=FEATURE_ID_PATTERN)),
#    Route('example.index.all_lects.alt',"/example/{feature_id}/{lect_id:all}.{extension}", requirements=dict(feature_id=FEATURE_ID_PATTERN)),
#    ]
#
#
#    # CUSTOM ROUTES HERE
#    #
#    # would the following make sense?
#    #map.redirect("/2008/{url:.*}", "/")
#    #
#    if config.get('wals.app_name') == 'wals':
#        # very specific hack to make genealogical language list available as supplement
#        map.redirect("/supplement/4", "/languoid/genealogy")
#        map.redirect("/supplement/4.{extension}", "/languoid/genealogy.{extension}")
#
#    # configuration dependent routes:
#    for route in [
#        Redirect("/static/"+config.get('wals.app_name')+"/descriptions/{id}/images/{filename}",
#                 "/chapter/{id:\d+}/images/{filename}"),
#        ]:
#        route.connect(map)
#
#    map.redirect("/supplement/{id}/images/{filename}", "/static/"+config.get('wals.app_name')+"/descriptions/s{id}/images/{filename}")
#
#    #
#    # replace with supplement.citation, id=5
#    #
#    #map.connect('languoid.citation.genealogy', "/languoid/citation/{id:genealogy}",
#    #            controller='languoid',
#    #            action='citation')
#    #map.connect('languoid.citation.genealogy.alt', R"/languoid/citation/{id:genealogy}.{extension}",
#    #            requirements=dict(extension=EXTENSION_PATTERN),
#    #            controller='languoid',
#    #            action='citation')
#    #map.connect('languoid.citation', "/languoid/citation/"+WALS_CODE_PREFIX+"{id}",
#    #            requirements=dict(id=LECT_ID_PATTERN),
#    #            controller='languoid',
#    #            action='citation')
#    #map.connect('languoid.citation.alt', R"/languoid/citation/"+WALS_CODE_PREFIX+"{id}.{extension}",
#    #            requirements=dict(id=LECT_ID_PATTERN, extension=EXTENSION_PATTERN),
#    #            controller='languoid',
#    #            action='citation')
#
#    map.connect("static", "/static/{type}/{filename}", _static=True)
#    map.connect("static.project", "/static/{project}/{type}/{filename}", _static=True)
#    map.connect("static.description", "/static/"+config.get('wals.app_name')+"/descriptions/{id}/{filename}", _static=True)
#
#    map.connect("icon.default", "/static/"+config.get('wals.app_name')+"/images/icons/{id}.png", _static=True)
#    map.connect("refdbrecord.default", "http://"+config.get('wals.refdb.domain', 'localhost')+"/refdb/record/{id}", _static=True)
#
#    map.redirect("/register/unapi", "/chapter/unapi")
#
#    map.connect("blog.category", "http://"+config.get('wals.blog.domain', 'localhost')+"/category/{cat}/", _static=True)
#    map.connect("blog.post", "http://"+config.get('wals.blog.domain', 'localhost')+"/{slug}/", _static=True)
#
#    map.connect("sil", "http://www.sil.org/iso639-3/documentation.asp?id={id}", _static=True)
#    map.connect('ethnologue', "http://www.ethnologue.com/show_language.asp?code={id}", _static=True)
#    map.connect("olacsubject", "http://www.language-archives.org/REC/field.html", _static=True)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    settings['route_patterns'] = {
        'languages': '/languoid',
        'language': '/languoid/lect/wals_code_{id:[^/\.]+}',
        'source': '/refdb/record/{id:[^/\.]+}',
        'sources': '/refdb',
        'familys': '/languoid',
        'family': '/languoid/family/{id:[^/\.]+}',
        'genus': '/languoid/genus/{id:[^/\.]+}',
        'parameters': '/feature',
        'parameter': '/feature/{id:[^/\.]+}',
        'sentences': '/example',
        'sentence': '/example/{id:[^/\.]+}',
        'contributions': '/chapter',
        'contribution': '/chapter/{id:[^/\.]+}',
        'countrys': '/country',
        'country': '/country/{id:[^/\.]+}',
        'contributors': '/author',
        'contributor': '/author/{id:[^/\.]+}',
        'legal': '/about/legal',
        'olac': '/languoid/oai',
        'credits': '/about/credits',
    }
    settings['sitemaps'] = 'contribution parameter source sentence valueset'.split()

    convert = lambda spec: ''.join(c if i == 0 else c + c for i, c in enumerate(spec))
    filename_pattern = re.compile('(?P<spec>(c|d|s|f|t)[0-9a-f]{3})\.png')
    icons = {}
    for name in sorted(
        path(__file__).dirname().joinpath('static', 'icons').files()
    ):
        m = filename_pattern.match(name.splitall()[-1])
        if m:
            icons[m.group('spec')] = convert(m.group('spec'))
    settings['icons'] = icons

    utilities = [
        (WalsCtxFactoryQuery(), ICtxFactoryQuery),
        (map_marker, IMapMarker),
        (Blog(settings), IBlog),
    ]
    config = get_configurator('wals3', *utilities, **dict(settings=settings))
    config.register_menu(
        ('dataset', partial(menu_item, 'dataset', label='Home')),
        ('parameters', partial(menu_item, 'parameters')),
        ('contributions', partial(menu_item, 'contributions')),
        ('languages', partial(menu_item, 'languages')),
        ('sources', partial(menu_item, 'sources')),
        #('examples', partial(menu_item, 'sentences')),
        ('contributors', partial(menu_item, 'contributors')),
        ('blog', lambda ctx, req: (req.blog.url('category/news/'), 'Newsblog')),
    )

    config.include('wals3.maps')
    config.include('wals3.datatables')

    config.register_resource('family', Family, IFamily)
    config.register_adapter(adapter_factory('family/detail_html.mako'), IFamily)

    config.register_resource('genus', Genus, IGenus)
    config.register_adapter(adapter_factory('genus/detail_html.mako'), IGenus)

    config.register_resource('country', Country, ICountry)
    config.register_adapter(adapter_factory('country/detail_html.mako'), ICountry)

    config.add_route('sample', '/languoid/samples/{count}', factory=sample_factory)

    config.register_adapter(GeoJsonFeature, IParameter)
    config.add_route('feature_info', '/feature-info/{id}')
    config.add_route('genealogy', '/languoid/genealogy')

    config.add_301(
        '/index',
        lambda req: req.route_url('dataset'))
    config.add_301(
        '/.{ext}',
        lambda req: req.route_url('dataset_alt', ext=req.matchdict['ext']))

    # we redirect legacy urls for datapoints because they could not be expressed
    # with a single id.
    def datapoint(req):
        data = {k: v for k, v in req.matchdict.items()}
        if data['fid'][-1] not in ascii_uppercase:
            data['fid'] += 'A'
        return req.route_url('valueset', id='%(fid)s-%(lid)s' % data)

    config.add_301('/datapoint/{fid}/wals_code_{lid}', datapoint, name='datapoint')
    config.add_301(
        "/feature/description/{id:[0-9]+}",
        lambda req: req.route_url('contribution', id=req.matchdict['id']))

    config.add_301('/languoid/lect', lambda req: req.route_url('languages'))
    config.add_301('/languoid/family', lambda req: req.route_url('languages'))
    config.add_301('/languoid/genus', lambda req: req.route_url('languages'))

    for pattern in ['/refdb/', '/refdb/record', '/refdb/record/', '/refdb/search']:
        config.add_301(pattern, lambda req: req.route_url('sources'))

    config.add_410('/languoid/osd.{ext}')
    config.add_410("/experimental/{id}")

    config.add_route('olac.source', '/refdb_oai')
    config.add_route('languoids', '/languoids')
    return config.make_wsgi_app()
