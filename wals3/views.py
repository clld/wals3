from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError


@view_config(route_name='home', renderer='home.mako')
def my_view(request):
    return {}
