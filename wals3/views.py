from datetime import datetime
from itertools import groupby

from sqlalchemy import or_, and_
from sqlalchemy.orm import joinedload_all, joinedload
from sqlalchemy.inspection import inspect
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPMovedPermanently, HTTPFound
from pytz import utc

from clld.db.meta import DBSession
from clld.db.models.common import Value, ValueSet
from wals3.models import Family, Genus, Feature


@view_config(route_name='feature_info', renderer='json')
def info(request):
    feature = Feature.get(request.matchdict['id'])
    return {
        'name': feature.name,
        'values': [{'name': d.name, 'number': i + 1} for i, d in enumerate(feature.domain)],
    }


@view_config(route_name='datapoint')
def datapoint(request):
    return HTTPMovedPermanently(
        request.route_url('valueset', id='%(fid)s-%(lid)s' % request.matchdict))


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


@view_config(route_name="changes", renderer="changes.mako")
def changes(request):
    """
    select vs.id, v.updated, h.domainelement_pk, v.domainelement_pk from value_history as h, value as v, valueset as vs where h.pk = v.pk and v.valueset_pk = vs.pk;
    """
    # changes in the 2011 edition: check values with an updated date after 2011 and before 2013
    E2009 = utc.localize(datetime(2009, 1, 1))
    E2012 = utc.localize(datetime(2012, 1, 1))

    history = inspect(Value.__history_mapper__).class_
    query = DBSession.query(Value, history)\
        .join(ValueSet)\
        .filter(Value.pk == history.pk)\
        .order_by(ValueSet.parameter_pk, ValueSet.language_pk)\
        .options(joinedload_all(Value.valueset, ValueSet.language))

    changes2011 = query.filter(or_(
        and_(E2009 < Value.updated, Value.updated < E2012),
        and_(E2009 < history.updated, history.updated < E2012)))

    changes2013 = query.filter(or_(
        E2012 < Value.updated, E2012 < history.updated))

    return {
        'changes2011': groupby([v.valueset for v, h in changes2011], lambda vs: vs.parameter),
        'changes2013': groupby([v.valueset for v, h in changes2013], lambda vs: vs.parameter)}


@view_config(route_name='sample', renderer='sample.mako')
def sample(ctx, request):
    return {'ctx': ctx}
