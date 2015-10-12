# coding=utf-8
"""australian

Revision ID": 36897f06d33c
Revises": 2b7ebbbcaf7c
Create Date": 2015-10-09 15":42":16.169860

"""
from __future__ import unicode_literals

from alembic import op

from clld.util import slug
from clld.db.models.common import Config, Language

from wals3.migration import Connection
from wals3.models import Genus, Family, WalsLanguage


# revision identifiers, used by Alembic.
revision = '36897f06d33c'
down_revision = u'2b7ebbbcaf7c'


GONE = [
    "westerndaly",  # dff4400
    "southerndaly",  # fffffcc
    "westbarkly",  # s99ffff
    "pamanyungan",  # faa0000
    "maran",  # scccccc
]
DATA = {
    "Northern Daly": {
        "northerndaly": [
            "Malakmalak",
            "Tyeraity",
        ],
    },
    "Western Daly": {  # genus westerndaly gone
        ("wagaydy", "Wagaydy", "fffffcc"): [  # new
            "Emmi",
            "Maranungku",
        ],
        ("bringen", "Bringen", "faa0000"): [  # new
            "Marrithiyel",
            "Maringarr",
        ],
    },
    "Eastern Daly": {
        "easterndaly": [
            "Madngele",
            "Kamu",
        ],
    },
    "Southern Daly": {  # genus southerndaly gone
        "murrinhpatha": [
            "Murrinh-Patha",
        ],
        ("ngankikurungkurr", "Ngankikurungkurr", "fffffcc"): [  # new
            "Ngankikurungkurr",
            "Ngan'gityemerri",
        ],
    },
    "Anson Bay": {
        "ansonbay": [
            "Bachamal",
            "Pungupungu",
        ],
    },
    "Gunwinyguan": {
        "anindilyakwa": [
            "Anindilyakwa",
        ],
        "nunggubuyu": [
            "Nunggubuyu",
        ],
        "ngalakan": [
            "Ngalakan",
        ],
        "ngandi": [
            "Ngandi",
        ],
        "rembarnga": [
            "Rembarnga",
        ],
        "gunwinygic": [
            "Bininj Gun-Wok",
            "Gunbalang",
            "Ngalkbun",
        ],
        ("waray", "Warayic"): [  # rename current genus Waray
            "Waray (in Australia)",
        ],
    },
    "Mangarrayi-Maran": {  # maran genus gone
        "mangarrayi": [
            "Mangarrayi",
        ],
        ("alawa", "Alawa", "sffffcc"): [  # new genus
            "Alawa",
        ],
        ("mara", "Mara", "saa0000"): [  # new genus
            "Mara",
        ],
        ("warndarang", "Warndarang", "scccccc"): [  # new genus
            "Warndarang",
        ],
    },
    "Mangrida": {
        "burarran": [
            "Burarra",
            "Gurr-goni"
        ],
        "nakkara": [
            "Nakkara",
        ],
        "ndjebbana": [
            "Ndjébbana",
        ],
    },
    "Mirndi": {
        "jaminjungan": [
            "Jaminjung"
        ],
        ("djingili", "Djingili", "fffffcc"): [  # new genus
            "Djingili"
        ],
        ("wambayan", "Wambayan", "faa0000"): [  # new genus
            "Wambaya"
        ],
    },
    "Darwin Region": {
        ("laragiyan", "Laragia"): [  # rename laragiyan genus
            "Laragia"
        ],
        "limilngan": [
            "Limilngan"
        ],
    },
    "Pama-Nyungan": {
        ("centralpamanyungan", "Central Pama-Nyungan", "tcccccc"): [  # new genus
            "Adynyamathanha",
            "Alyawarra",
            "Arabana",
            "Arrernte",
            "Arrernte (Mparntwe)",
            "Arrernte (Western)",
            "Banggarla",
            "Diyari",
            "Innamincka",
            "Kaurna",
            "Kaytej",
            "Paakantyi",
            "Pitta Pitta",
            "Wangkangurru",
            "Wangkumara",
            "Wirangu",
        ],
        ("westernpamanyungan", "Western Pama-Nyungan", "t99ffff"): [  # new genus
            "Badimaya",
            "Balyku",
            "Bayungu",
            "Bilinarra",
            "Bularnu",
            "Dhalandji",
            "Dhargari",
            "Dhuwal (Dätiwuy)",
            "Djambarrpuyngu",
            "Djapu",
            "Djaru",
            "Djinang",
            "Gaalpu",
            "Gugada",
            "Gumatj",
            "Gupapuyngu",
            "Gurindji",
            "Karadjeri",
            "Kariera",
            "Mantjiltjara",
            "Martu Wangka",
            "Martuthunira",
            "Mirniny",
            "Mudburra",
            "Ngaanyatjarra",
            "Ngadjumaja",
            "Ngarinyman",
            "Ngarla",
            "Ngarluma",
            "Nhanda",
            "Nyamal",
            "Nyangumarda",
            "Nyungar",
            "Juat",
            "Panyjima",
            "Pintupi",
            "Pitjantjatjara",
            "Ritharngu",
            "Walmatjari",
            "Wanman",
            "Warlpiri",
            "Warluwara",
            "Warumungu",
            "Watjarri",
            "Western Desert (Ooldea)",
            "Yankuntjatjara",
            "Yanyuwa",
            "Yindjibarndi",
            "Yingkarta",
            "Yulparija",
        ],
        ("northernpamanyungan", "Northern Pama-Nyungan", "taa0000"): [  # new genus
            "Anguthimri",
            "Biri",
            "Dharumbal",
            "Djabugay",
            "Dyirbal",
            "Gugadj",
            "Gunya",
            "Guugu Yimidhirr",
            "Kala Lagaw Ya",
            "Kalkatungu",
            "Kugu Nganhcara",
            "Kuku-Yalanji",
            "Kunjen",
            "Kuuk Thaayorre",
            "Kuuku Ya'u",
            "Lamu-Lamu",
            "Linngithig",
            "Margany",
            "Mayi-Yapi",
            "Mbabaram",
            "Ngawun",
            "Nyawaygi",
            "Pakanha",
            "Thaypan",
            "Umpila",
            "Uradhi",
            "Warrgamay",
            "Warrongo",
            "Wik Munkan",
            "Wik Ngathana",
            "Yalarnnga",
            "Yidiny",
            "Yir Yiront",
        ],
        ("southeasternpamanyungan", "Southeastern Pama-Nyungan", "tffffcc"): [
            "Bandjalang",
            "Bandjalang (Casino)",
            "Bandjalang (Waalubal)",
            "Bandjalang (Yugumbir)",
            "Colac",
            "Dharawal",
            "Dhurga",
            "Gamilaraay",
            "Gidabal",
            "Gumbaynggir",
            "Gureng Gureng",
            "Madimadi",
            "Muruwari",
            "Ngarinyeri",
            "Ngiyambaa",
            "Wagawaga",
            "Warrnambool",
            "Wathawurrung",
            "Wembawemba",
            "Woiwurrung",
            "Yaygir",
            "Yorta Yorta",
            "Yuwaalaraay",
        ],
    },
    "Jarrakan": {
        ("djeragan", "Jarrakan"): [  # rename djeragan
            "Miriwung",
            "Kitja"
        ]
    },
    "Worrorran": {
        ("wororan", "Worrorran"): [  # rename wororan
            "Gunin",
            "Worora",
            "Ungarinjin",
        ]
    },
    "Bunuban": {"bunuban": []},  # 2
    "Gaagudju": {"gaagudju": []},  # 1
    "Garrwan": {"garrwan": []},  # 1
    "Iwaidjan": {"iwaidjan": []},  # 2
    "Nyulnyulan": {"nyulnyulan": []},  # 5
    "Tangkic": {"tangkic": []},  # 3
    "Tiwian": {"tiwian": []},  # 1
    "Wagiman": {"wagiman": []},  # 1
    "Yangmanic": {"yangmanic": []},  # 1
}  # + 17


def upgrade():
    conn = Connection(op.get_bind())

    for fname, genera in DATA.items():
        fpk = conn.insert(Family, id=slug(fname), name=fname)

        for gspec, lnames in genera.items():
            if isinstance(gspec, tuple):
                if len(gspec) == 3:
                    # new genus
                    gpk = conn.insert(
                        Genus, id=gspec[0], name=gspec[1], icon=gspec[2], family_pk=fpk)
                elif len(gspec) == 2:
                    # rename genus
                    gpk = conn.pk(Genus, gspec[0])
                    conn.update(Genus, dict(family_pk=fpk, name=gspec[1]), pk=gpk)
                else:
                    raise ValueError()
            else:
                # just update the family
                gpk = conn.pk(Genus, gspec)
                conn.update(Genus, dict(family_pk=fpk), pk=gpk)

            for lname in lnames:
                lpk = conn.pk(Language, lname, attr='name')
                conn.update(WalsLanguage, dict(genus_pk=gpk), pk=lpk)

    for gid in GONE:
        conn.insert(Config, key=Config.replacement_key(Genus, gid), value=Config.gone)
        conn.delete(Genus, id=gid)

    conn.insert(
        Config, key=Config.replacement_key(Family, 'australian'), value=Config.gone)
    conn.delete(Family, id='australian')

    conn.update_name('mdl', 'Matngele')


def downgrade():
    pass
