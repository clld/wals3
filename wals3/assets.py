from clld.web.assets import environment
from path import path

import wals3


environment.append_path(
    path(wals3.__file__).dirname().joinpath('static'), url='/wals3:static/')
environment.load_path = list(reversed(environment.load_path))
