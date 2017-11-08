# coding=ascii
"""reassign iso codes glottocodes and el names

Revision ID: 299f89bc1fc1
Revises: 15da24f7a5af
Create Date: 2017-11-08 15:45:42.050000

"""
from __future__ import unicode_literals

# revision identifiers, used by Alembic.
revision = '299f89bc1fc1'
down_revision = u'15da24f7a5af'

import string
import datetime

from alembic import op
import sqlalchemy as sa

ID_BEFORE_AFTER = { # https://github.com/clld/wals-data/issues/107
    'aci': {
        'name': (u'Ach\xed', None),
        'iso': (['acc', 'acr'], 'acr'),
        'gcode': (['quic1275'], 'achi1256'),
        'elname': (["Achi', Cubulco", "Achi', Rabinal"], 'Achi'),
    },
    'pkm': {
        'name': (u'Pokomch\xed', None),
        'iso': (['pob', 'poh'], 'poh'),
        'gcode': (['poco1241'], 'poqo1254'),
        'elname': (["Poqomchi', Eastern", "Poqomchi', Western"], "Poqomchi'"),
    },
    'gam': {
        'name': ('Gamo', None),
        'iso': (['gmo'], 'gmv'),
        'gcode': (['gamo1244'], 'gamo1243'),
        'elname': (['Gamo-Gofa-Dawro'], 'Gamo'),
    },
    'sum': {
        'name': ('Sumu', 'Mayangna'),
        'iso': (['sum'], 'yan'),
        'gcode': (['sumo1243'], 'maya1285'),
        'elname': (['Sumo-Mayangna'], 'Mayangna'),
    },
    'tzo': {
        'name': ('Tzotzil', None),
        'iso': (['tzc'], 'tzo'),
        'gcode': (['tzot1262'], 'tzot1259'),
        'elname': (['Tzotzil, Chamula'], 'Tzotzil'),
    },
    'ixi': {
        'name': ('Ixil', None),
        'iso': (['ixi', 'ixl'], 'ixl'),
        'gcode': (['ixil1250'], 'ixil1251'),
        'elname': (['Ixil, Nebaj', 'Ixil, San Juan Cotzal'], 'Ixil'),
    },
    'bem': {
        'name': ('Bemba', None),
        'iso': (['bmy'], 'bem'),
        'gcode': (['bemb1258'], 'bemb1257'),
    },
    'htc': {
        'name': ('Huastec', None),
        'iso': (['hsf'], 'hus'),
        'gcode': (['huas1256'], 'huas1242'),
        'elname': (['Huastec, Southeastern'], 'Huastec'),
    },
    'kyq': {
        'name': ('Kyuquot', None),
        'iso': (['noo'], 'nuk'),
        'gcode': (['noot1239'], 'nuuc1236'),
        'elname': (['Nootka'], 'Nuu-chah-nulth'),
    },
    'nit': {
        'name': ('Nitinaht', None),
        'iso': (['noo'], 'dtd'),
        'gcode': (['noot1239'], 'diti1235'),
        'elname': (['Nootka'], 'Ditidaht'),
    },
    'tzu': {
        'name': ('Tzutujil', None),
        'iso': (['tzj', 'tzt'], 'tzj'),
        'gcode': (['cakc1244'], 'tzut1248'),
        'elname': ([u'Tz\u2019utujil, Eastern', u'Tz\u2019utujil, Western'], "Tz'utujil"),
    },
    'vla': {
        'name': ('Vlaamse Gebarentaal', None),
        'iso': (['bvs'], 'vgt'),
        'gcode': (['vlaa1235'], None),
        'elname': ([], 'Flemish Sign Language'),
    },
    'nlr': {
        'name': ('Ngarla', None),
        'iso': (['nlr'], 'nrk'),
        'gcode': (['ngar1286'], None),
    },
    'nax': {
        'name': ('Naxi', None),
        'iso': (['nbf'], 'nxq'),
        'gcode': (['naxi1245'], None),
    },
    'akm': {
        'name': ('Arakanese (Marma)', None),
        'iso': (['mhv'], 'rmz'),
        'gcode': (['marm1234'], None),
        'elname': ([], 'Marma'),
    },
    'cak': {
        'name': ('Cakchiquel', None),
        'iso': (['ckf'], 'cak'),
        'gcode': (['kaqc1274'], 'kaqc1270'),
        'elname': (['Kaqchikel, Southern'], 'Kaqchikel'),
    },
    'nbk': {
        'name': (u'Nat\xfcgu', None),
        'iso': (['stc'], 'ntu'),
        'gcode': (['natu1249'], 'natu1246'),
    },
    'tnn': {
        'name': ('Tunen', None),
        'iso': (['baz'], 'tvu'),
        'gcode': (['tune1241'], 'tune1261'),
    },
    'itb': {
        'name': ('Italian (Bologna)', None),
        'iso': (['eml'], 'egl'),
        'gcode': (['emil1242'], 'emil1241'),
        'elname': (['Emiliano-Romagnolo'], 'Emilian'),
    },
    'yir': {
        'name': ('Yir Yiront', None),
        'iso': (['yiy'], 'yyr'),
        'gcode': (['yiry1245'], 'yiry1247'),
    },
    'nis': {
        'name': ('Nyishi', None),
        'iso': (['dap'], 'njz'),
        'gcode': (['nisi1239'], 'nyis1236'),
        'elname': (['Nisi'], 'Nyishi'),
    },
    'yug': {
        'name': ('Yugh', None),
        'iso': (['yuu'], 'yug'),
        'gcode': (['yugh1239'], None),
        'elname': (['Yugh'], 'Yug'),
    },
    'ptw': {
        'name': ('Patwin', None),
        'iso': (['wit'], 'pwu'),
        'gcode': (['wint1259'], 'patw1250'),
        'elname': (['Wintu'], 'Patwin'),
    },
    'win': {
        'name': ('Wintu', None),
        'iso': (['wit'], 'wnw'),
        'gcode': (['wint1259'], None),
    },
    'grr': {
        'name': ('Garrwa', None),
        'iso': (['gbc'], 'wrk'),
        'gcode': (['gara1261'], 'gara1269'),
        'elname': (['Garawa'], 'Garrwa'),
    },
    'gla': {
        'name': ('Gelao', None),
        'iso': (['gio'], 'gqu'),
        'gcode': (['gela1261'], 'qaua1234'),
        'elname': (['Gelao'], 'Qau'),
    },
    'wan': {
        'name': ('Wangkumara', None),
        'iso': (['nbx'], 'xwk'),
        'gcode': (['ngur1261'], None),
        'elname': (['Ngura'], 'Wangkumara'),
    },
    'izi': {
        'name': ('Izi', None),
        'iso': (['izi'], 'izz'),
        'gcode': (['izie1238'], None),
        'elname': (['Izi-Ezaa-Ikwo-Mgbo'], 'Izii'),
    },
    'ish': {
        'name': ('Ishkashmi', None),
        'iso': (['sgl'], 'isk'),
        'gcode': (['sang1316'], 'sang1236'),
        'elname': (['Sanglechi-Ishkashimi'], 'Ishkashmi'),
    },
    'wor': {
        'name': ('Worora', None),
        'iso': (['unp'], 'wro'),
        'gcode': (['woro1255'], None),
        'elname': (['Worora'], 'Worrorra'),
    },
    'mdb': {
        'name': ('Mudburra', None),
        'iso': (['mwd'], 'dmw'),
        'gcode': (['mudb1240'], None),
        'elname': (['Mudbura'], 'Mudburra'),
    },
    'mhc': {
        'name': ('Mahican', None),
        'iso': (['mof'], 'xpq'),
        'gcode': (['mohe1244'], None),
        'elname': (['Mohegan-Montauk-Narragansett'], 'Mohegan-Pequot'),
    },
    'wir': {
        'name': ('Wirangu', None),
        'iso': (['wiw'], 'wgu'),
        'gcode': (['wira1265'], None),
    },
    'tga': {
        'name': ('Tangga', None),
        'iso': (['tgg'], 'hrc'),
        'gcode': (['tang1348'], None),
        'elname': (['Tangga'], 'Niwer Mil'),
    },
    'lng': {
        'name': ('Lengua', None),
        'iso': (['leg'], 'enx'),
        'gcode': (['leng1262'], None),
        'elname': (['Lengua'], 'Enxet'),
    },
    'nbd': {
        'name': ('Nubian (Dongolese)', None),
        'iso': (['kzh'], 'dgl'),
        'gcode': (['kenu1236'], None),
        'elname': (['Kenuzi-Dongola'], 'Andaandi'),
    },
    'nku': {
        'name': ('Nubian (Kunuz)', None),
        'iso': (['kzh'], 'xnz'),
        'gcode': (['kenu1236'], None),
        'elname': (['Kenuzi-Dongola'], 'Kenzi (Mattoki)'),
    },
}


def ascii_name(s, _whitelist=set(string.ascii_lowercase + ' ()0123456789')):
    assert all(ord(c) < 128 for c in s)
    return ''.join(c for c in s.lower() if c in _whitelist)


def upgrade():
    conn = op.get_bind()

    l = sa.table('language', *map(sa.column, ['pk', 'updated', 'id', 'name']))
    w = sa.table('walslanguage', *map(sa.column, ['pk', 'ascii_name']))

    lwhere = (l.c.id == sa.bindparam('id_'))

    update_lang = l.update(bind=conn).where(lwhere)\
        .where(l.c.name == sa.bindparam('before'))\
        .values(updated=sa.func.now(), name=sa.bindparam('after'))

    update_wals = w.update(bind=conn)\
        .where(sa.exists().where(w.c.pk == l.c.pk).where(lwhere))\
        .where(w.c.ascii_name == sa.bindparam('ascii_before'))\
        .values(ascii_name=sa.bindparam('ascii_name'))

    icols = ['created', 'updated', 'active', 'version', 'id', 'type', 'description', 'lang', 'name']
    i = sa.table('identifier', *map(sa.column, ['pk'] + icols))

    licols = ['created', 'updated', 'active', 'version', 'language_pk', 'identifier_pk']
    li = sa.table('languageidentifier', *map(sa.column, licols))

    t_iso, t_gl, t_nam = (sa.bindparam('type', t) for t in ['iso639-3', 'glottolog', 'name'])
    d_el = sa.bindparam('description', 'ethnologue')
    iwheres_itdl = [
        ('iso', i.c.type == t_iso, [sa.bindparam('after'), t_iso, None, sa.literal('en')]),
        ('gcode', i.c.type == t_gl, [sa.bindparam('after'), t_gl, None, sa.literal('en')]),
        ('elname', sa.and_(i.c.type == t_nam, i.c.description == d_el), [None, t_nam, d_el, sa.literal('en')]),
    ]

    l_pk = sa.select([l.c.pk]).where(lwhere).as_scalar()
    before, after = map(sa.bindparam, ['before', 'after'])

    def unlink_insert_link(iw, itdl):
        liwhere = sa.exists()\
            .where(li.c.language_pk == l.c.pk).where(lwhere)\
            .where(li.c.identifier_pk == i.c.pk).where(iw)

        unlink_li = li.delete(bind=conn)\
            .where(liwhere.where(i.c.name.op('IN')(before)).where(i.c.name != after))

        insert_i = i.insert(bind=conn).from_select(icols,
            sa.select([sa.func.now(), sa.func.now(), True, 1] + itdl + [after])
            .where(~sa.exists().where(iw).where(i.c.name == after)))

        i_pk = sa.select([i.c.pk]).where(iw).where(i.c.name == after).as_scalar()

        link_li = li.insert(bind=conn).from_select(licols,
            sa.select([sa.func.now(), sa.func.now(), True, 1, l_pk, i_pk])
            .where(~liwhere.where(i.c.name == after)))

        return unlink_li, insert_i, link_li

    field_ops = [(f, unlink_insert_link(iw, itdl)) for f, iw, itdl in iwheres_itdl]

    for id_, fields in sorted(ID_BEFORE_AFTER.items()):
        name_before, name_after = fields.pop('name')
        if name_after is not None:
            update_lang.execute(id_=id_, before=name_before, after=name_after)
            update_wals.execute(id_=id_, ascii_before=ascii_name(name_before), ascii_name=ascii_name(name_after))
        for f, (unlink, insert, link) in field_ops:
            before, after = fields.get(f, (None, None))
            if after is not None:
                if before:
                    unlink.execute(id_=id_, before=tuple(before), after=after)
                insert.execute(after=after)
                link.execute(id_=id_, after=after)


def downgrade():
    pass
