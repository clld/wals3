from collections import defaultdict
from tempfile import mktemp

from path import path
from mock import Mock, patch
from pyramid.httpexceptions import HTTPFound

from clld.tests.util import TestWithEnv, TestWithDb
from clld.interfaces import IBlog
from clld.db.models.common import ValueSet, Language
from clld.db.meta import DBSession

import wals3


class Tests2(TestWithDb):
    __with_custom_language__ = False

    def test_migration(self):
        from wals3.migration import Connection

        conn = Connection(DBSession)
        conn.insert(Language, id='zzz')
        conn.update_iso('zzz', 'deu', eng='English')
        conn.update_iso('zzz', 'eng', deu='German')
        conn.update_genus('zzz', ('genus', u'Genus', ''), ('family', u'Family'))
        conn.update_genus('zzz', ('othergenus', u'Other Genus', ''), 'family')
        conn.update_genus('zzz', 'genus')


class Tests(TestWithEnv):
    __cfg__ = path(wals3.__file__).dirname().joinpath('..', 'development.ini').abspath()
    __setup_db__ = False
    __with_custom_language__ = False

    def test_comment(self):
        from wals3.views import comment

        self.env['registry'].registerUtility(Mock(post_url=lambda *a, **kw: '/'), IBlog)
        self.set_request_properties(matchdict=dict(fid='51A', lid='esm'))
        self.assertIsInstance(comment(self.env['request']), HTTPFound)

    def test_Blog(self):
        from wals3.blog import Blog

        vs = ValueSet.first()

        class wp(object):
            def __init__(self, cats=False):
                if cats:
                    self.cats = [
                        dict(id=1, name='Languages'),
                        dict(id=2, name='Chapters'),
                        dict(id=3, name=vs.parameter.chapter.area.name),
                    ]
                else:
                    self.cats = []

            def Client(self, *args, **kw):
                return Mock(
                    get_categories=lambda: self.cats,
                    set_categories=lambda c: dict(n=1),
                    get_post_id_from_path=lambda p: None)

        with patch('wals3.blog.wordpress', wp()):
            blog = Blog(defaultdict(lambda: ''))
            blog.post_url(vs, self.env['request'], create=True)

        with patch('wals3.blog.wordpress', wp(cats=True)):
            blog = Blog(defaultdict(lambda: ''))
            blog.post_url(vs, self.env['request'], create=True)

    def test_Matrix(self):
        from wals3.adapters import Matrix

        p = path(mktemp())
        assert not p.exists()

        class TestMatrix(Matrix):
            def abspath(self, req):
                return p

            def query(self, req):
                return Matrix.query(self, req).filter(Language.pk < 100)

        m = TestMatrix(Language, 'wals3', description="Feature values CSV")
        m.create(self.env['request'], verbose=False)
        assert p.exists()
        p.remove()
