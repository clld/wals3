from collections import defaultdict

from path import path
from mock import Mock, patch
from pyramid.httpexceptions import HTTPFound

from clld.tests.util import TestWithEnv
from clld.interfaces import IBlog
from clld.db.models.common import ValueSet

import wals3


class Tests(TestWithEnv):
    __cfg__ = path(wals3.__file__).dirname().joinpath('..', 'development.ini').abspath()
    __setup_db__ = False

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
