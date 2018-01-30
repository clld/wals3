import pytest

from pyramid.response import Response
from clld.db.meta import DBSession


@pytest.mark.parametrize(
    "method,path",
    [
        ('get_html', '/'),
        ('get_html', '/combinations/55A_89A'),
        ('get_html', '/feature-info/3A'),
        ('get_html', '/changes'),
        ('get_xml', '/refdb_oai?verb=Identify'),
        ('get_html', '/languoid/genealogy'),
        ('get_html', '/languoid/samples/100'),
        ('get_html', '/languoid/samples/200'),
        ('get_json', '/languoid/samples/100.json'),
        ('get_json', '/languoid/samples/200.json'),
        ('get_html', '/languoid/lect/wals_code_apk'),
        ('get_html', '/chapter/144'),
        ('get_html', '/feature/2A'),
        ('get_html', '/languoid/family/afroasiatic'),
        ('get_html', '/country/ID'),
        ('get_html', '/languoid'),
        ('get_html', '/languoid.map.html'),
        ('get_html', '/languoid/genus/berber'),
        ('get_html', '/languoid/family/arawakan'),
        ('get_html', '/chapter'),
        ('get_dt', '/chapter?iSortingCols=1&iSortCol_0=0'),
        ('get_dt', '/feature?sSearch_3=pho&iSortingCols=1&iSortCol_0=3'),
        ('get_dt', '/values?iSortingCols=1&iSortCol_0=1&sSortDir_0=desc'),
        ('get_dt', '/languoid?sSearch_8=Australia'),
        ('get_dt', '/values?parameter=1A'),
        ('get_dt', '/values?parameter=1A&v1=c000'),
        ('get_dt', '/values?language=eng&iSortingCols=1&iSortCol_0=4'),
        ('get_dt', '/values?language=eng&sSearch_1=noun&iSortingCols=1&iSortCol_0=1'),
        ('get_dt', '/values?language=eng&sSearch_4=phon'),
    ])
def test_pages(app, method, path):
    getattr(app, method)(path)


def test_samples(app):
    app.get('/languoid/samples/x', status=404)


def test_resources(app):
    app.get('/chapter/s4', status=302)


def test_g(app):
    app.get_dt('/languoid?sSearch_8=Australia')
    app.get('/languoid.tab')

    app.get('/languoids?id=g-berber', status=302)
    app.get('/languoids?id=f-arawakan', status=302)
    app.get('/languoids?id=w-abh', status=302)
    app.get_json('/languoids?q=')
    app.get_json('/languoids?q=berbery')
    app.get_json('/languoids?q=berber')
    app.get_json('/languoids?q=austronesian')
    app.get('/languoids?id=gberber', status=404)
    app.get('/languoids?id=x-berber', status=404)
    app.get('/languoids?id=g-berberyyy', status=404)


def test_feature(app):
    _path = '/feature?iSortingCols=1&iSortCol_0='
    app.get_dt(_path + '0')
    app.get_dt(_path + '1')
    for ext in 'geojson georss tab xml kml'.split():
        get = app.get
        if ext in ['georss', 'xml', 'kml']:
            get = app.get_xml
        elif ext in ['geojson']:
            get = app.get_json
        get('/feature/2A.%s?domainelement=2A-1' % ext)
    app.get('/feature/2A?lat=20.2&lng=-20.2&z=5')
    app.get('/feature/2A?z=zoom')


def test_misc(app):
    app.get_xml('/feature/12A.rdf')
    app.get_xml('/languoid/lect/wals_code_akb.rdf')
    app.get_xml('/chapter/12.rdf')
    app.get('/feature/20', status=301)
    app.get('/refdb/record/5', status=301)
    app.get('/refdb/record/555555', status=404)
    app.get_html('/refdb/record/Abega-1970')
    app.get_html('/feature/20A.snippet.html?v1=c000', docroot='div')
    if str(DBSession.get_bind().url).startswith('postgresql'):
        app.get_html('/combinations/1A_2A?v1=c000')
    app.get_html('/languoid/family/sepik?sepikhill=c000')


def test_redirects(app):
    app.get('/feature/combined/1A/2A', status=301)
    app.get('/datapoint/1/wals_code_aab', status=301)


def test_olac(app):
    p = '/refdb_oai?verb='
    md = '&metadataPrefix=olac'
    app.get_xml(p + 'GetRecord&identifier=oai:refdb.wals.info:1' + md)
    app.get_xml(p + 'ListRecords&from=1900-01-01' + md)
    app.get_xml(p + 'ListRecords&until=1900-01-01' + md)
    app.get_xml(p + 'Identify')
    p = '/languoid/oai?verb='
    md = '&metadataPrefix=olac'
    app.get_xml(p + 'GetRecord&identifier=oai:wals.info:languoid:cea' + md)
    app.get_xml(p + 'ListRecords&until=3000-01-01' + md)
    app.get_xml(p + 'Identify')


def test_blog_feed(app, mocker):
    app.get('/blog', status=404)
    mocker.patch('wals3.views.atom_feed', mocker.Mock(return_value=Response('test')))
    assert 'test' in app.get('/blog?path=test')
