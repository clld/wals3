from datetime import datetime
from itertools import groupby

from sqlalchemy import or_, and_
from sqlalchemy.orm import joinedload_all, joinedload
from sqlalchemy.inspection import inspect
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPMovedPermanently, HTTPFound, HTTPNotFound
from pytz import utc

from clld.db.meta import DBSession
from clld.db.models.common import Value, ValueSet, Source, Language, LanguageIdentifier, Identifier, Parameter
from clld.db.util import icontains
from clld.web.views.olac import OlacConfig, olac_with_cfg, Participant, Institution

from wals3.models import Family, Genus, Feature, WalsLanguage
from wals3.util import LanguoidSelect



"""
http://wals.info/feature/82A?s=20&v1=c00d&v2=cd00&v3=cccc&z1=2998&z2=2999&z3=3000&tg_format=map&lat=5.5&lng=152.58&z=2&t=m
"""


@view_config(route_name='languoids', renderer='json')
def languoids(request):
    if request.params.get('id'):
        if not '-' in request.params['id']:
            return HTTPNotFound()
        m, id_ = request.params['id'].split('-', 1)
        model = dict(w=Language, g=Genus, f=Family).get(m)
        if not model:
            return HTTPNotFound()
        obj = model.get(id_)
        if not obj:
            return HTTPNotFound()
        return HTTPFound(location=request.resource_url(obj))

    max_results = 20
    qs = request.params.get('q')
    if not qs:
        return []

    query = DBSession.query(Language)\
        .filter(icontains(Language.name, qs))\
        .order_by(WalsLanguage.ascii_name).limit(max_results)

    res = [l for l in query]

    if len(res) < max_results:
        max_results = max_results - len(res)

        # fill up suggestions with matching alternative names:
        for l in DBSession.query(Language)\
                .join(Language.languageidentifier, LanguageIdentifier.identifier)\
                .filter(icontains(Identifier.name, qs))\
                .order_by(WalsLanguage.ascii_name).limit(max_results):
            if l not in res:
                res.append(l)

    if len(res) < max_results:
        max_results = max_results - len(res)

        # fill up with matching genera:
        for l in DBSession.query(Genus)\
                .filter(icontains(Genus.name, qs))\
                .order_by(Genus.name).limit(max_results):
            res.append(l)

    if len(res) < max_results:
        max_results = max_results - len(res)

        # fill up with matching families:
        for l in DBSession.query(Family)\
                .filter(icontains(Family.name, qs))\
                .order_by(Family.name).limit(max_results):
            res.append(l)

    ms = LanguoidSelect(request, None, None, url='x')
    return dict(results=map(ms.format_result, res), context={}, more=False)


@view_config(route_name='feature_info', renderer='json')
def info(request):
    feature = Feature.get(request.matchdict['id'])
    return {
        'name': feature.name,
        'values': [{'name': d.name, 'number': i + 1} for i, d in enumerate(feature.domain)],
    }


@view_config(route_name='datapoint', request_method='POST')
def comment(request):
    """
    check whether a blog post for the datapoint does exist, if not, create one and
    redirect there.
    """
    vs = ValueSet.get('%(fid)s-%(lid)s' % request.matchdict)
    return HTTPFound(request.blog.post_url(vs, request, create=True) + '#comment')


@view_config(route_name='genealogy', renderer='genealogy.mako')
def genealogy(request):
    return dict(
        families=DBSession.query(Family).order_by(Family.id)\
        .options(joinedload_all(Family.genera, Genus.languages)))


def changes(request):
    """
    select vs.id, v.updated, h.domainelement_pk, v.domainelement_pk from value_history as h, value as v, valueset as vs where h.pk = v.pk and v.valueset_pk = vs.pk;
    """
    # changes in the 2011 edition: check values with an updated date after 2011 and before 2013
    E2009 = utc.localize(datetime(2009, 1, 1))
    E2012 = utc.localize(datetime(2012, 1, 1))

    history = inspect(Value.__history_mapper__).class_
    query = DBSession.query(Value)\
        .outerjoin(history, Value.pk == history.pk)\
        .join(ValueSet)\
        .order_by(ValueSet.parameter_pk, ValueSet.language_pk)\
        .options(joinedload_all(Value.valueset, ValueSet.language),
                 joinedload_all(Value.valueset, ValueSet.parameter))

    changes2011 = query.join(ValueSet.parameter)\
        .filter(Parameter.id.contains('A'))\
        .filter(Parameter.id != '143A')\
        .filter(Parameter.id != '144A')\
        .filter(or_(
            and_(E2009 < Value.updated, Value.updated < E2012),
            and_(history.updated != None, E2009 < history.updated, history.updated < E2012)))

    changes2013 = query.filter(or_(
        E2012 < Value.updated, E2012 < history.updated))

    return {
        'changes2011': groupby([v.valueset for v in changes2011], lambda vs: vs.parameter),
        'changes2013': groupby([v.valueset for v in changes2013], lambda vs: vs.parameter)}


@view_config(route_name='sample', renderer='sample.mako')
def sample(ctx, request):
    return {'ctx': ctx}


class OlacConfigSource(OlacConfig):
    def _query(self, req):
        return req.db.query(Source)

    def get_earliest_record(self, req):
        return self._query(req).order_by(Source.updated, Source.pk).first()

    def get_record(self, req, identifier):
        """
        """
        rec = Source.get(self.parse_identifier(req, identifier), default=None)
        assert rec
        return rec

    def query_records(self, req, from_=None, until=None):
        q = self._query(req).order_by(Source.pk)
        if from_:
            q = q.filter(Source.updated >= from_)
        if until:
            q = q.filter(Source.updated < until)
        return q

    def format_identifier(self, req, item):
        """
        """
        return self.delimiter.join([self.scheme, 'refdb.' + req.dataset.domain, str(item.pk)])

    def parse_identifier(self, req, id_):
        """
        """
        assert self.delimiter in id_
        return int(id_.split(self.delimiter)[-1])

    def description(self, req):
        return {
            'archiveURL': 'http://%s/refdb_oai' % req.dataset.domain,
            'participants': [
                Participant("Admin", 'Robert Forkel', 'robert_forkel@eva.mpg.de'),
            ] + [Participant("Editor", ed.contributor.name, ed.contributor.email or req.dataset.contact) for ed in req.dataset.editors],
            'institution': Institution(
                req.dataset.publisher_name,
                req.dataset.publisher_url,
                '%s, Germany' % req.dataset.publisher_place,
            ),
            'synopsis': 'The World Atlas of Language Structures Online is a large database '
            'of structural (phonological, grammatical, lexical) properties of languages '
            'gathered from descriptive materials (such as reference grammars). The RefDB '
            'archive contains bibliographical records for all resources cited in WALS Online.',
        }


@view_config(route_name='olac.source')
def olac_source(req):
    return olac_with_cfg(req, OlacConfigSource())
