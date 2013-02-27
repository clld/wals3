from path import path

from clld.tests.util import TestWithApp

import wals3


class Tests(TestWithApp):
    __cfg__ = path(wals3.__file__).dirname().joinpath('..', 'development.ini').abspath()
    __setup_db__ = False

    def test_home(self):
        res = self.app.get('/', status=200)

    def test_genealogy(self):
        res = self.app.get('/languoid/genealogy', status=200)

    def test_resources(self):
        for rsc, id_, index in [
            ('language', 'apk', True),
            ('contributor', None, True),
            ('contribution', '144', True),
            ('parameter', '2A', True),
            ('family', 'afroasiatic', False),
            ('country', 'ID', False),
        ]:
            if id_:
                res = self.app.get('/%s/%s' % (rsc, id_), headers={'accept': 'text/html'}, status=200)
            if index:
                res = self.app.get('/%ss' % rsc, headers={'accept': 'text/html'}, status=200)

                headers = {'x-requested-with': 'XMLHttpRequest'}
                _path = '/%ss?sEcho=1&iSortingCols=1&iSortCol_0=1&sSortDir_0=desc' % rsc
                res = self.app.get(_path, headers=headers, status=200)

        headers = {'x-requested-with': 'XMLHttpRequest'}
        _path = '/values?sEcho=1&iSortingCols=1&iSortCol_0=1&sSortDir_0=desc'
        res = self.app.get(_path, headers=headers, status=200)
