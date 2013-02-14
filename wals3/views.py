from sqlalchemy.orm import joinedload_all

from pyramid.response import Response
from pyramid.view import view_config

from clld.db.meta import DBSession
from wals3.models import Family, Genus, Feature


@view_config(route_name='home', renderer='home.mako')
def home(request):
    return {}


@view_config(route_name='feature_info', renderer='json')
def info(request):
    feature = Feature.get(request.matchdict['id'])
    return {
        'name': feature.name,
        'values': [{'name': d.name, 'number': i + 1} for i, d in enumerate(feature.domain)],
    }


@view_config(route_name='genealogy', renderer='genealogy.mako')
def genealogy(request):
    return dict(families=DBSession.query(Family).order_by(Family.id)\
        .options(joinedload_all(Family.genera, Genus.languages)))
