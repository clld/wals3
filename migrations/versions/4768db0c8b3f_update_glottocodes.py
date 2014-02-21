# coding=utf-8
"""update glottocodes

Revision ID: 4768db0c8b3f
Revises: 5397fbf9bc04
Create Date: 2014-02-21 13:56:58.846489

"""

# revision identifiers, used by Alembic.
revision = '4768db0c8b3f'
down_revision = '5397fbf9bc04'

import datetime

from alembic import op
import sqlalchemy as sa

from clld.db.migration import Connection


GLOTTOCODES = {
    "clc": "cola1237",
    "cut": "cuit1236",
    "kaq": "kaur1267",
    "vla": "vlaa1235",
    "yyo": "yort1237",
    "wwr": "woiw1237",
    "mcc": "moch1259",
    "puq": "puqu1242",
    "yyg": "yayg1236",
    "bti": "beto1236",
    "wrb": "warr1257",
    "bgn": "bugu1246",
    "bnu": "bula1255",
    "wth": "wath1238",
    "nha": "nhan1238",
    "nan": "nand1266",
    "akm": "marm1234",
    "guq": "cari1279",
    "isl": "inte1259",
    "nhp": "poch1244",
    "yrm": "yuru1243",
    "cco": "tutu1242",
    "hks": "hong1241",
    "ktt": "kott1239",
    "mpr": "maip1246",
    "alc": "alle1238",
    "luy": "saam1283",
    "esm": "atac1235",
    "mkw": "maku1246",
    "lul": "lule1238",
    "kwz": "kwaz1243",
    "jel": "jeri1242",
    "mbb": "mbab1239",
    "kno": "kano1245",
    "smp": "shom1245",
    "wom": "womo1238",
    "ksn": "suoy1242",
    "cuc": "timo1237",
    "myy": "mayk1239",
    "bso": "basq1250",
    "scr": "sout1528",
    "uzb": "uzbe1247",
    "aym": "nucl1667",
    "pkm": "poco1241",
    "tzu": "cakc1244",
    "gur": "guru1261",
    "kis": "kiss1245",
    "maz": "maza1293",
    "sla": "slav1253",
    "tze": "tzel1253",
    "chj": "chuj1249",
    "ctc": "cuic1234",
    "giz": "maro1246",
    "gue": "guer1240",
    "ixi": "ixil1250",
    "kew": "kewa1250",
    "nua": "nuau1240",
    "qbo": "boli1262",
    "shp": "nort1527",
    "tuk": "tuka1247",
    "dgi": "indo1311",
    "bvi": "bali1280",
    "col": "chol1281",
    "aci": "quic1275",
    "crt": "chor1274",
    "ene": "enet1250",
    "agm": "anga1287",
    "hai": "haid1248",
    "hmo": "huam1250",
    "jin": "jino1236",
    "kmb": "ndei1235",
    "kol": "kola1242",
    "kpw": "east2341",
    "ktu": "nucl1297",
    "nhh": "huas1257",
    "plg": "nucl1291",
    "pum": "pumi1242",
    "qia": "qian1264",
    "kkv": "kali1298",
    "srb": "sorb1249",
    "sti": "stie1250",
    "tbu": "tebu1238",
    "tou": "tusi1238",
    "baa": "bara1377",
    "biu": "bisu1246",
    "blz": "bala1300",
    "ydd": "yidd1255",
    "wah": "wahg1249",
    "cea": "swam1239",  # TODO: remove obsolete iso code (!= csw) as well!
}


def upgrade():
    conn = Connection(op.get_bind())
    for lid, glottocode in GLOTTOCODES.items():
        conn.set_glottocode(lid, glottocode)


def downgrade():
    pass
