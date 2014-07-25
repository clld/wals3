from path import path

from clld.tests.util import TestWithApp
from clld.db.meta import DBSession

import wals3


class Tests(TestWithApp):
    __cfg__ = path(wals3.__file__).dirname().joinpath('..', 'development.ini').abspath()
    __setup_db__ = False

    def test_home(self):
        self.app.get_html('/')
        self.app.get_html('/feature-info/3A')
        self.app.get_html('/changes')
        self.app.get_xml('/refdb_oai?verb=Identify')

    def test_genealogy(self):
        self.app.get_html('/languoid/genealogy')

    def test_samples(self):
        for count in [100, 200]:
            self.app.get_html('/languoid/samples/%s' % count)
        self.app.get('/languoid/samples/x', status=404)

    def test_resources(self):
        for _path in [
            '/languoid/lect/wals_code_apk',
            '/chapter/144',
            '/feature/2A',
            '/languoid/family/afroasiatic',
            '/country/ID',
        ]:
            self.app.get_html(_path)
        self.app.get('/chapter/s4', status=302)
        self.app.get_dt('/values?iSortingCols=1&iSortCol_0=1&sSortDir_0=desc')

    def test_g(self):
        self.app.get_html('/languoid')
        self.app.get_dt('/languoid?sSearch_8=Australia')
        self.app.get('/languoid.tab')
        self.app.get_html('/languoid.map.html')
        self.app.get_html('/languoid/genus/berber')
        self.app.get_html('/languoid/family/arawakan')

        self.app.get('/languoids?id=g-berber', status=302)
        self.app.get('/languoids?id=f-arawakan', status=302)
        self.app.get('/languoids?id=w-abh', status=302)
        self.app.get_json('/languoids?q=')
        self.app.get_json('/languoids?q=berbery')
        self.app.get_json('/languoids?q=berber')
        self.app.get_json('/languoids?q=austronesian')
        self.app.get('/languoids?id=gberber', status=404)
        self.app.get('/languoids?id=x-berber', status=404)
        self.app.get('/languoids?id=g-berberyyy', status=404)

    def test_feature(self):
        _path = '/feature?iSortingCols=1&iSortCol_0='
        self.app.get_dt(_path + '0')
        self.app.get_dt(_path + '1')
        for ext in 'geojson georss tab xml kml solr.json'.split():
            get = self.app.get
            if ext in ['georss', 'xml', 'kml']:
                get = self.app.get_xml
            elif ext in ['geojson', 'solr.json']:
                get = self.app.get_json
            get('/feature/2A.%s?domainelement=2A-1' % ext)
        self.app.get('/feature/2A?lat=20.2&lng=-20.2&z=5')
        self.app.get('/feature/2A?z=zoom')

    def test_misc(self):
        self.app.get_xml('/feature/12A.rdf')
        self.app.get_xml('/languoid/lect/wals_code_akb.rdf')
        self.app.get_xml('/chapter/12.rdf')
        self.app.get('/feature/20', status=301)
        self.app.get('/refdb/record/5', status=301)
        self.app.get('/refdb/record/555555', status=404)
        self.app.get_html('/refdb/record/Abega-1970')
        self.app.get_html('/feature/20A.snippet.html?v1=c000', docroot='div')
        if str(DBSession.get_bind().url).startswith('postgresql'):
            self.app.get_html('/combinations/1A_2A?v1=c000')
        self.app.get_html('/languoid/family/sepik?sepikhill=c000')

    def test_redirects(self):
        self.app.get('/feature/combined/1A/2A', status=301)
        self.app.get('/datapoint/1/wals_code_aab', status=301)

    def test_olac(self):
        p = '/refdb_oai?verb='
        md = '&metadataPrefix=olac'
        self.app.get_xml(p + 'GetRecord&identifier=oai:refdb.wals.info:1' + md)
        self.app.get_xml(p + 'ListRecords&from=1900-01-01' + md)
        self.app.get_xml(p + 'ListRecords&until=1900-01-01' + md)
        self.app.get_xml(p + 'Identify')
        p = '/languoid/oai?verb='
        md = '&metadataPrefix=olac'
        self.app.get_xml(p + 'GetRecord&identifier=oai:wals.info:languoid:cea' + md)
        self.app.get_xml(p + 'ListRecords&until=3000-01-01' + md)
        self.app.get_xml(p + 'Identify')

    def test_features(self):
        self.app.get_dt('/feature?sSearch_3=pho&iSortingCols=1&iSortCol_0=3')

    def test_chapters(self):
        self.app.get_html('/chapter')
        self.app.get_dt('/chapter?iSortingCols=1&iSortCol_0=0')

    def test_values(self):
        self.app.get_dt('/values?parameter=1A')
        self.app.get_dt('/values?parameter=1A&v1=c000')
        self.app.get_dt('/values?language=eng&iSortingCols=1&iSortCol_0=4')
        self.app.get_dt('/values?language=eng&sSearch_1=noun&iSortingCols=1&iSortCol_0=1')
        self.app.get_dt('/values?language=eng&sSearch_4=phon')
