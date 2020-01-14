import pathlib

from clld.web.assets import environment

import wals3


environment.append_path(
    str(pathlib.Path(wals3.__file__).parent.joinpath('static')), url='/wals3:static/')
environment.load_path = list(reversed(environment.load_path))
