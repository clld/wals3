import codecs

from path import path

import wals3


def get_description(req, contribution):
    p = path(wals3.__file__).dirname().joinpath('static', 'descriptions', str(contribution.id), 'body.xhtml')
    c = codecs.open(p, encoding='utf8').read()
    return c.replace('http://wals.info', req.application_url)
