import codecs
import re
from xml.etree import ElementTree as et
from sqlite3.dbapi2 import connect

from path import path
from bs4 import BeautifulSoup as soup

import wals3

c = connect('/home/robert/old_projects/legacy/wals_pylons/trunk/wals2/db.sqlite')
cu = c.cursor()
cu.execute('select id, family_id from genus')
GENUS_MAP = dict(cu.fetchall())


def pattern(path):
    return re.compile('http\:\/\/wals\.info' + path)

def url(path):
    return 'http://wals.info' + path

URL_PATTERNS = {
    'country': (
        pattern('\/languoid\/by_geography\?country\=(?P<id>[A-Z]{2})$'),
        lambda m: url('/country/%s' % m.group('id')),
    ),
    'genus': (
        pattern('\/languoid\/genus\/(?P<id>[a-z]+)$'),
        lambda m: url('/family/%s#%s' % (GENUS_MAP[m.group('id')], m.group('id'))),
    ),
    'family': (
        pattern('\/languoid\/family\/(?P<id>[a-z]+)$'),
        lambda m: url('/family/%s' % m.group('id')),
    ),
    'source': (
        pattern('\/refdb\/record\/(?P<id>.+)$'),
        lambda m: url('/source/%s' % m.group('id')),
    ),
    'contribution': (
        pattern('\/feature\/(description\/)?(?P<id>[0-9]+)(?P<fragment>\#.*)?$'),
        lambda m: url('/contribution/%s%s' % (m.group('id'), m.group('fragment') or '')),
    ),
    'parameter': (
        pattern('\/feature\/(?P<id>[0-9]+[A-Z])'),
        lambda m: url('/parameter/%s' % m.group('id')),
    ),
    'language': (
        pattern('\/languoid\/lect\/wals_code_(?P<id>[a-z]{2,3})$'),
        lambda m: url('/language/%s' % m.group('id')),
    ),
    'image': (
        re.compile('\.\/(?P<id>.+)\/images\/(?P<path>.+)$'),
        lambda m: url('/static/descriptions/%(id)s/images/%(path)s' % m.groupdict()),
    ),
}


def fix(id_):
    print('chapter %s' % id_)
    p = path(wals3.__file__).dirname().joinpath(
        'static', 'descriptions', str(id_), 'body.html')
    assert p.exists()
    r = codecs.open(p, encoding='utf8').read()
    et.fromstring(r.encode('utf8'))
    s = soup(r)

    #
    # fix URLs
    #
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

    #
    # fix examples
    #
    in_example = False
    for tag in s.find_all('p', class_=True):
        if 'example-start' in tag.attrs['class']:
            in_example = True

        if 'example-end' in tag.attrs['class']:
            assert in_example
            in_example = False

    assert not in_example

    #
    # TODO: replace span class="T3" with tooltip showing the meaning of the gloss part!
    # use css and javascript from valency!
    #

    #
    # handle value tables
    #
    for tag in s.find_all('div', class_='value-table'):
        tag.name = 'table'
        tag['class'] = ['table', 'table-hover', 'values']
        tag['style'] = 'width: auto;'
        tag.string = '__values_%s__' % tag['id'].split('-')[-1]

        for sibling in tag.parent.previous_siblings:
            if getattr(sibling, 'name', None) == 'p':
                if 'captionValueTable' in sibling.get('class', []):
                    sibling.name = 'caption'
                    del sibling['class']
                    tag.insert(0, sibling.extract())
                break

    for tag in s.find_all('div', id=True):
        if re.match('values\_[A-Z]$', tag['id']):
            tag.extract()

    for tag in s.find_all('span', class_='close'):
        if 'onclick' in tag.attrs:
            tag.extract()

    for tag in s.find_all('li', style=True):
        del tag['style']

    for tag in s.find_all('ul', id='tableofcontent'):
        tag['class'] = 'nav nav-tabs nav-stacked'.split()

    #
    # cleanup tables
    #
    for tag in s.find_all('table', class_="Table1"):
        if tag.find('td', class_="tableBox"):
            tag['class'] = "table table-bordered".split()
        else:
            tag['class'] = "table table-hover".split()
        for attr in 'cellpadding border cellspacing'.split():
            del tag[attr]

    for tag in s.find_all('td', class_="tableHeader"):
        tag.name = 'th'
        del tag['class']

    for class_ in ["tableTopRow", "tableInside", "tableBottomRow", "tableBox"]:
        for tag in s.find_all('td', class_=class_):
            del tag['class']
            if class_ == 'tableBox':
                for _t in tag.find_all('p', style=True):
                    del _t['style']
                for _t in tag.find_all('ul', style=True):
                    del _t['style']

    #
    # put captions inside the table
    #
    for tag in s.find_all('p', class_="captionTable"):
        div = None
        table = None
        for sibling in tag.next_siblings:
            if getattr(sibling, 'name', None) == 'div':
                div = sibling
                break
            if getattr(sibling, 'name', None) == 'table':
                table = sibling
                break
        if div:
            table = div.find('table')
        if table:
            caption = tag.extract()
            caption.name = 'caption'
            del caption['class']
            table.insert(0, caption)

    #
    # figures
    #
    for class_ in ["figureChapter", "figureExample"]:
        for tag in s.find_all('div', class_=class_):
            tag.name = 'figure'
            del tag['class']

    for tag in s.find_all('p', class_="captionFigure"):
        tag.name = 'figcaption'
        for attr in tag.attrs.keys():
            del tag[attr]

    #c = s.prettify()
    c = unicode(s)
    c = c.replace('<?xml version="1.0"?>\n', '').strip()
    c = re.sub(
        '\<p\s+class\=\"example\-start\"\>',
        '<blockquote class="example"><p class="example-start">',
        c,
        flags=re.M)
    c = re.sub(
        u'\<p\s+class\=\"example\-end\"\>[\s\xa0]*\<\/p\>',
        '<p class="example-end"></p></blockquote>',
        c,
        flags=re.M)

    try:
        et.fromstring(c.encode('utf8'))
    finally:
        with open(p.dirname().joinpath('body.xhtml'), 'w') as fp:
            fp.write(c.encode('utf8'))


if __name__ == '__main__':
    map(fix, range(1, 145))
