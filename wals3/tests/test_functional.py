from path import path

from clld.tests.util import TestWithApp

import wals3


class Tests(TestWithApp):
    __cfg__ = path(wals3.__file__).dirname().joinpath('..', 'development.ini').abspath()
    __setup_db__ = False

    def test_home(self):
        self.app.get('/', status=200)
        self.app.get('/feature-info/3A')
        self.app.get('/changes')
        self.app.get('/refdb_oai?verb=Identify')

    def test_genealogy(self):
        self.app.get('/languoid/genealogy', status=200)

    def test_samples(self):
        for count in [100, 200]:
            self.app.get('/languoid/samples/%s' % count, status=200)
        self.app.get('/languoid/samples/x', status=404)

    def test_resources(self):
        for path in [
            '/languoid/lect/wals_code_apk',
            '/chapter/144',
            '/feature/2A',
            '/languoid/family/afroasiatic',
            '/country/ID',
        ]:
            self.app.get(path, accept='text/html', status=200)
            #if index:
            #    self.app.get('/%ss' % rsc, headers={'accept': 'text/html'}, status=200)

            #    headers = {'x-requested-with': 'XMLHttpRequest'}
            #    _path = '/%ss?sEcho=1&iSortingCols=1&iSortCol_0=1&sSortDir_0=desc' % rsc
            #    self.app.get(_path, headers=headers, status=200)
        self.app.get('/chapter/s4', status=302)

        _path = '/values?sEcho=1&iSortingCols=1&iSortCol_0=1&sSortDir_0=desc'
        self.app.get(_path, xhr=True, status=200)

    def test_g(self):
        self.app.get('/languoid')
        self.app.get('/languoid.tab')
        self.app.get('/languoid.map.html')
        self.app.get('/languoid/genus/berber')
        self.app.get('/languoid/family/arawakan')

        self.app.get('/languoids?id=g-berber')
        self.app.get('/languoids?id=f-arawakan')
        self.app.get('/languoids?id=w-abh')
        self.app.get('/languoids?q=')
        self.app.get('/languoids?q=berbery')
        self.app.get('/languoids?q=berber')
        self.app.get('/languoids?id=gberber', status=404)
        self.app.get('/languoids?id=x-berber', status=404)
        self.app.get('/languoids?id=g-berberyyy', status=404)

    def test_feature(self):
        _path = '/feature?sEcho=1&iSortingCols=1&iSortCol_0='
        self.app.get(_path + '0', xhr=True, status=200)
        self.app.get(_path + '1', xhr=True, status=200)
        for ext in 'geojson georss tab xml kml solr.json'.split():
            self.app.get('/feature/2A.%s?domainelement=2A-1' % ext, status=200)

    def test_misc(self):
        self.app.get('/feature/12A.rdf', status=200)
        self.app.get('/languoid/lect/wals_code_aab.rdf', status=200)
        self.app.get('/chapter/12.rdf', status=200)
        self.app.get('/feature/20', status=301)
        self.app.get('/refdb/record/5', status=301)
        self.app.get('/refdb/record/555555', status=404)
        self.app.get('/refdb/record/Abega-1970', status=200)
        self.app.get('/values?parameter=1A&sEcho=1', xhr=True, status=200)
        self.app.get('/values?parameter=1A&v1=c000&sEcho=1', xhr=True, status=200)
        self.app.get('/feature/20A.snippet.html?v1=c000', status=200)
        self.app.get('/languoid/family/sepik?sepikhill=c000', status=200)

    def test_redirects(self):
        self.app.get('/feature/combined/1A/2A', status=301)
        self.app.get('/datapoint/1/wals_code_aab', status=301)
        #self.app.get('', status=301)

    def test_olac(self):
        p = '/refdb_oai?verb='
        md = '&metadataPrefix=olac'
        self.app.get(p+'GetRecord&identifier=oai:refdb.wals.info:1'+md, status=200)
        self.app.get(p + 'ListRecords' + md, status=200)
        self.app.get(p + 'Identify', status=200)
        p = '/languoid/oai?verb='
        md = '&metadataPrefix=olac'
        self.app.get(p+'GetRecord&identifier=oai:wals.info:languoid:cea'+md, status=200)
        self.app.get(p + 'ListRecords' + md, status=200)
        self.app.get(p + 'Identify', status=200)
