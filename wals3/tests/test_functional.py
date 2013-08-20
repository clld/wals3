from path import path

from clld.tests.util import TestWithApp

import wals3


class Tests(TestWithApp):
    __cfg__ = path(wals3.__file__).dirname().joinpath('..', 'development.ini').abspath()
    __setup_db__ = False

    def test_home(self):
        self.app.get('/', status=200)

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

        _path = '/values?sEcho=1&iSortingCols=1&iSortCol_0=1&sSortDir_0=desc'
        self.app.get(_path, xhr=True, status=200)
