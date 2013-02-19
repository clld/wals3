import codecs
import re
from xml.etree import ElementTree as et
from sqlite3.dbapi2 import connect

from purl import URL
from path import path
from bs4 import BeautifulSoup as soup

import wals3

c = connect('/home/robert/old_projects/legacy/wals_pylons/trunk/wals2/db.sqlite')
cu = c.cursor()
cu.execute('select id, family_id from genus')
GENUS_MAP = dict(cu.fetchall())


URL_PATTERNS = {
    'country': (
        re.compile('http\:\/\/wals\.info\/languoid\/by_geography\?country\=(?P<id>[A-Z]{2})$'),
        lambda m: 'http://wals.info/country/%s' % m.group('id'),
    ),
    'genus': (
        re.compile('http\:\/\/wals\.info\/languoid\/genus\/(?P<id>[a-z]+)$'),
        lambda m: 'http://wals.info/family/%s#%s' % (GENUS_MAP[m.group('id')], m.group('id')),
    ),
    'family': (
        re.compile('http\:\/\/wals\.info\/languoid\/family\/(?P<id>[a-z]+)$'),
        lambda m: 'http://wals.info/family/%s' % m.group('id'),
    ),
    'source': (
        re.compile('http\:\/\/wals\.info\/refdb\/record\/(?P<id>.+)$'),
        lambda m: 'http://wals.info/source/%s' % m.group('id'),
    ),
    'parameter': (
        re.compile('http\:\/\/wals\.info\/feature\/(?P<id>[0-9]+(?P<letter>[A-Z])?)'),
        lambda m: 'http://wals.info/parameter/%s%s' % (m.group('id'), '' if m.group('letter') else 'A'),
    ),
    'language': (
        re.compile('http\:\/\/wals\.info\/languoid\/lect\/wals_code_(?P<id>[a-z]{2,3})$'),
        lambda m: 'http://wals.info/language/%s' % m.group('id'),
    ),
    'image': (
        re.compile('\.\/(?P<id>.+)\/images\/(?P<path>.+)$'),
        lambda m: 'http://wals.info/static/descriptions/%(id)s/images/%(path)s' % m.groupdict(),
    ),
}


def fix(id_):
    print('chapter %s' % id_)
    p = path(wals3.__file__).dirname().joinpath('static', 'descriptions', str(id_), 'body.html')
    assert p.exists()
    r = codecs.open(p, encoding='utf8').read()
    s = soup(r)

    for attrname, tagname in [('href', 'a'), ('src', 'img')]:
        for tag in s.find_all(tagname, **{attrname: True}):
            replaced = False
            attr = tag[attrname].strip()
            if attr.startswith('#'):
                continue
            for _p, _r in URL_PATTERNS.values():
                m = _p.match(attr)
                if m:
                    tag[attrname] = _r(m)
                    replaced = True
                    break
            if not replaced:
                print(attr)

    in_example = False
    for tag in s.find_all('p', class_=True):
        if 'example-start' in tag.attrs['class']:
            in_example = True

        if 'example-end' in tag.attrs['class']:
            assert in_example
            in_example = False

    assert not in_example

    c = s.prettify()
    c = c.replace('<?xml version="1.0"?>\n', '').strip()
    c = c.replace('<p class="example-start">', '<blockquote>\n<p class="example-start">')
    c = re.sub('\<p class\=\"example\-end\"\>\s*</p>', '<p class="example-end">\n</p>\n</blockquote>', c, flags=re.M)

    et.fromstring(c.encode('utf8'))

    with open(p.dirname().joinpath('body.xhtml'), 'w') as fp:
        fp.write(c.encode('utf8'))


if __name__ == '__main__':
    map(fix, range(1, 145))
