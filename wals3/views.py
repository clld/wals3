from pyramid.response import Response
from pyramid.view import view_config

from clld.db.meta import DBSession
from wals3.models import Family


@view_config(route_name='home', renderer='home.mako')
def home(request):
    return {}

