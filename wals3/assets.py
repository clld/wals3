from clld.web.assets import environment
from clldutils.path import Path

import wals3


environment.append_path(
    Path(wals3.__file__).parent.joinpath('static').as_posix(), url='/wals3:static/')
environment.load_path = list(reversed(environment.load_path))
