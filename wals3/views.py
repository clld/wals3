from pyramid.response import Response
from pyramid.view import view_config

from wals3.models import Family, Feature


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
