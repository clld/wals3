# coding: utf8
from __future__ import unicode_literals
import re
from uuid import uuid1

from path import path
from sqlalchemy.orm.exc import NoResultFound
from clld.db.models import common
from clld.util import slug

from wals3 import models
import wals3


class Icons(object):
    filename_pattern = re.compile('(?P<spec>(c|d|s|f|t)[0-9a-f]{3})\.png')

    @staticmethod
    def id(spec):
        """translate old wals icon id into clld icon id c0a9 -> c00aa99
        """
        return ''.join(c if i == 0 else c + c for i, c in enumerate(spec))

    def __init__(self):
        self._icons = []
        for name in sorted(
            path(wals3.__file__).dirname().joinpath('static', 'icons').files()
        ):
            m = self.filename_pattern.match(name.splitall()[-1])
            if m:
                self._icons.append(Icons.id(m.group('spec')))

    def __iter__(self):
        return iter(self._icons)

ICONS = Icons()


def delete(session, obj, replacement=None, model=None):
    common.Config.add_replacement(obj, replacement, model=model, session=session)
    session.delete(obj)


def merge_sources(session, timestamp, s1, s2, *attrs):
    s1 = common.Source.get(s1, session=session)
    s2 = common.Source.get(s2, session=session)
    for attr in attrs:
        setattr(s2, attr, getattr(s1, attr))
    s2.updated = timestamp

    for attr in ['sentencereferences', 'contributionreferences', 'valuesetreferences']:
        for ref in getattr(s1, attr):
            ref.source = s2

    delete(session, s1, replacement=s2)


def get_vs(session, vs):
    if isinstance(vs, basestring):
        pid, lid = vs.split('-')
        return session.query(common.ValueSet)\
            .join(common.Parameter)\
            .join(common.Language)\
            .filter(common.Parameter.id == pid)\
            .filter(common.Language.id == lid)\
            .one()
    return vs


def vs_switch_lang(session, timestamp, vs, lang):
    if isinstance(lang, basestring):
        lang = common.Language.get(lang, session=session)
    vs1 = get_vs(session, vs)
    pid, lid = vs1.id.split('-')

    id_ = '-'.join([pid, lang.id])
    try:
        vs2 = get_vs(session, id_)
        vs2.updated = timestamp
    except NoResultFound:
        vs2 = common.ValueSet(
            id=id_,
            description=vs1.description,
            language=lang,
            parameter=vs1.parameter,
            contribution=vs1.contribution,
            updated=timestamp,
            created=timestamp,
            source=vs1.source)

    session.add(vs2)

    v1 = vs1.values[0]
    if vs2.values:
        assert v1.domainelement == vs2.values[0].domainelement
    else:
        session.add(common.Value(
            id=vs2.id,
            valueset=vs2,
            domainelement=v1.domainelement,
            created=timestamp,
            updated=timestamp))
    delete(session, v1)

    for ref in vs1.references:
        ref.valueset = vs2
    delete(session, vs1)


def vs_copy_lang(session, timestamp, vs, lang):
    if isinstance(lang, basestring):
        lang = common.Language.get(lang, session=session)
    vs1 = get_vs(session, vs)
    pid, lid = vs1.id.split('-')

    id_ = '-'.join([pid, lang.id])
    try:
        vs2 = get_vs(session, id_)
        vs2.updated = timestamp
        raise AssertionError
    except NoResultFound:
        vs2 = common.ValueSet(
            id=id_,
            description=vs1.description,
            language=lang,
            parameter=vs1.parameter,
            contribution=vs1.contribution,
            updated=timestamp,
            created=timestamp,
            source=vs1.source)

    session.add(vs2)

    # copy values and references:
    session.add(common.Value(
        id=vs2.id,
        valueset=vs2,
        domainelement=vs1.values[0].domainelement,
        created=timestamp,
        updated=timestamp))

    for ref in vs1.references:
        session.add(common.ValueSetReference(
            valueset=vs2,
            source=ref.source,
            key=ref.key,
            description=ref.description))


def vs_delete(session, timestamp, vs):
    vs = get_vs(session, vs)
    delete(session, vs.values[0])
    for ref in vs.references:
        session.delete(ref)
    delete(session, vs)


def update_iso(session, timestamp, lang, *obsolete, **new):
    if isinstance(lang, basestring):
        lang = common.Language.get(lang, session=session)
    lang.updated = timestamp

    for code in obsolete:
        for li in lang.languageidentifier:
            if li.identifier.id == code or li.identifier.id == 'ethnologue-' + code:
                session.delete(li)

    for code, name in new.items():
        iso = common.Identifier.get(code, session=session, default=None)
        ethnologue = common.Identifier.get('ethnologue-' + code, session=session, default=None)

        if not iso:
            iso = common.Identifier(
                id=code, name=code, description=name, type=common.IdentifierType.iso.value)

        if not ethnologue:
            ethnologue = common.Identifier(
                id='ethnologue-' + code, name=name, description='ethnologue', type='name')

        if iso.id not in [li.identifier.id for li in lang.languageidentifier]:
            session.add(common.LanguageIdentifier(language=lang, identifier=iso))

        if ethnologue.id not in [li.identifier.id for li in lang.languageidentifier]:
            session.add(common.LanguageIdentifier(language=lang, identifier=ethnologue))
    return lang


def update_glottocode(session, timestamp, lang, gc):
    if isinstance(lang, basestring):
        lang = common.Language.get(lang, session=session)
    lang.updated = timestamp

    for li in lang.languageidentifier:
        if li.identifier.name == gc and li.identifier.type == common.IdentifierType.glottolog.value:
            session.delete(li)

    glottocode = session.query(common.Identifier)\
        .filter(common.Identifier.type == common.IdentifierType.glottolog.value)\
        .filter(common.Identifier.name == gc)\
        .first()

    if not glottocode:
        glottocode = common.Identifier(
            id=gc, name=gc, description=gc, type=common.IdentifierType.glottolog.value)
    session.add(common.LanguageIdentifier(language=lang, identifier=glottocode))
    return lang


def update_classification(session,
                          timestamp,
                          langs,
                          genus_id,
                          genus_name=None,
                          family_id=None,
                          family_name=None,
                          subfamily=None):
    if family_id:
        family = models.Family.get(family_id, session=session, default=None)
        if not family:
            assert family_name
            family = models.Family(id=family_id, name=family_name)
    else:
        family = None

    genus = models.Genus.get(genus_id, session=session, default=None)
    if not genus:
        assert genus_name and family
        icons = [g.icon for g in family.genera]
        for icon in ICONS:
            if icon not in icons:
                break
        genus = models.Genus(
            id=genus_id,
            name=genus_name,
            family=family,
            subfamily=subfamily,
            icon=icon)

    for lang in langs:
        if isinstance(lang, basestring):
            lang = common.Language.get(lang, session=session)
        lang.updated = timestamp
        lang.genus = genus


def update_language(session, timestamp, lang, keep_old_name=False, **kw):
    if isinstance(lang, basestring):
        lang = common.Language.get(lang, session=session)

    if 'name' in kw and keep_old_name:
        name = common.Identifier(
            id=str(uuid1()), name=lang.name, description='other', type='name')
        session.add(common.LanguageIdentifier(language=lang, identifier=name))

    return update_obj(session, timestamp, lang, **kw)


def update_obj(session, timestamp, obj, **kw):
    obj.updated = timestamp
    for k, v in kw.items():
        setattr(obj, k, v)
    return obj


#
# issues
#
def issue5(session, timestamp):
    gul = update_iso(session, timestamp, 'gul', 'glu', kcm='Gula (Central African Republic)')
    update_glottocode(session, timestamp, gul, 'gula1266')


def issue7(session, timestamp):
    """
    wals3=# select id, name from language where name like 'Dangal%';
    id | name
    -----+---------------------
    dnw | Dangaléat (Western)
    (1 row)

    wals3=# select id, name from identifier where name like 'Dangal%';
    id | name
    ----------------+--------------------
    | Dangaleat, Western
    ethnologue-daa | Dangaléat
    (2 rows)
    """
    lang = update_language(session, timestamp, 'dnw', name='Dangaléat', ascii_name='dangaleat')
    for li in lang.languageidentifier:
        if 'Western' in li.identifier.name:
            id_ = li.identifier
            session.delete(li)
            session.delete(id_)


def issue8(session, timestamp):
    """
    It turns out that the data and sources for Yi (wals code yi) are actually for two
    completely different languages (both in the Burmese-Lolo genus, but in different branches).

    One language is Nuosu. We will keep the WALS code yi for Nuosu. We need to add Yi as
    a name under "Other". Its location needs to be changed to 28° N, 103° E. Otherwise,
    the language information remains the same.

    The other language is Nasu, whose information is as follows:
    Ethnologue name: Nasu
    ISO-code: ywq
    Ruhlen name: --
    Other name: Yi
    WALS code: nsu
    Location: 26° 10′ N, 102° 20′ E

    The source for Nuosu is
    Yiyu Jianzhi. [A brief description of the Yi language] by Chen Shilin, Bian Shiming and Xiuqing, Li 1985
    Chen-et-al-1985
    while the source for Nasu is
    Yiyu yufa yanjiu [A study on Yi grammar] by Gao, Huanian 1958
    Gao-1958
    """
    nuosu = update_language(
        session, timestamp, 'yi', keep_old_name=True,
        name='Nuosu', ascii_name='nuosu', latitude=28, longitude=103)

    nasu = models.WalsLanguage(
        id='nsu',
        name='Nasu',
        ascii_name='nasu',
        latitude=26.16666666666666666,
        longitude=102.33333333333333333,
        genus=nuosu.genus)
    update_iso(session, timestamp, nasu, ywq='Wuding-Luquan Yi')
    update_glottocode(session, timestamp, nasu, 'wudi1238')

    gao = common.Source.get('Gao-1958', session=session)
    for vs in nuosu.valuesets:
        if gao in [ref.source for ref in vs.references]:
            if len(vs.references) > 1:
                vs_copy_lang(session, timestamp, vs, nasu)
            else:
                vs_switch_lang(session, timestamp, vs, nasu)


def issue9(session, timestamp):
    """
    the location of Bao'an is inaccurate. It should be changed to 35° 45′ N, 102° 50′ E.
    """
    update_language(session, timestamp, 'bao', latitude=35.75, longitude=102.8333333333333334)


def issue10(session, timestamp):
    """
    1. Nubian (Hill) -> Ghulfan. In the case of Ghulfan, we need to add Nubian (Hill) to the
    list of names under Other.
    2. Kaguru -> Kagulu
    3. Gallong -> Galo. The name "Gallong" should be added under "Other".
    4. The name of the family and genus that Haruai belongs to should be changed to Piawi.
    5. Koyra -> Koorete.
    6. there is a spelling error in the name of the genus Jingpho, which contains one
    language with the same name. The name of the language is spelled correctly, but the
    genus is incorrectly spelled Jinghpo.
    7. The language Embera (wals code emb) should be renamed Emberá (Northern)
    """
    update_language(session, timestamp, 'nbh', keep_old_name=True,
                    name='Ghulfan', ascii_name='ghulfan')
    update_language(session, timestamp, 'kgr', name='Kagulu', ascii_name='kagulu')
    update_language(session, timestamp, 'gal', keep_old_name=True,
                    name='Galo', ascii_name='galo')
    genus = update_obj(session, timestamp, models.Genus.get('upperyuat', session=session), name='Piawi')
    update_obj(session, timestamp, genus.family, name='Piawi')
    update_language(session, timestamp, 'kjr', name='Koorete', ascii_name='koorete')
    update_obj(session, timestamp, models.Genus.get('jinghpo', session=session), name='Jingpho')
    update_language(session, timestamp, 'emb', name='Emberá (Northern)', ascii_name='embera northern')


def issue11(session, timestamp):
    """
    Another name change:
    Kaugel (kgl) -> Umbu Ungu
    with Kaugel added as a name under 'Other".

    Another name change:
    Bobo Fing [bbf] -> Bobo Madaré (Northern)

    Plus the current entry links Bobo Fing to two Ethnologue languages and two ISO codes,
    but this entry should link only to Konabéré and ISO code bbo.
    location for Bobo Fing [bbf] should be changed to
    12° 25′ N, 4° 20′ W
    """
    update_language(session, timestamp, 'kgl', keep_old_name=True,
                    name='Umbu Ungu', ascii_name='umbu ungu')

    bbf = update_language(
        session, timestamp, 'bbf',
        name='Bobo Madaré (Northern)',
        ascii_name='bobo madare northern',
        latitude=12.4166666666666667,
        longitude=-4.3333333333333)
    update_iso(session, timestamp, bbf, 'bwq')
    update_glottocode(session, timestamp, bbf, 'nort2819')


def issue13(session, timestamp):
    """
    The name for what is now called Tamang should be changed to Tamang (Eastern).
    (We are splitting it into two varieties, but we will not add Western Tamang yet.)
    It would keep the WALS code tam.
    The location should be changed to 27° 30′ N, 85° 40′ E .
    The references to Taylor 1973 should be removed (since that source is on the western variety).
    """
    tam = common.Language.get('tam', session=session)
    tam.updated = timestamp
    tam.name = "Tamang (Eastern)"
    tam.ascii_name = "tamang eastern"
    tam.latitude = 27.5
    tam.longitude = 85.666666666667

    taylor = common.Source.get('Taylor-1973', session=session)
    for vs in tam.valuesets:
        for ref in vs.references:
            if ref.source == taylor:
                session.delete(ref)


def issue14(session, timestamp):
    update_classification(
        session, timestamp,
        ['dhm'],
        'dhimalic', genus_name='Dhimalic', family_id='sinotibetan', subfamily='Tibeto-Burman')


def issue15(session, timestamp):
    """
    the following languages should also be removed from Bodic and put into a new genus
    (also within the Tibeto-Burman subfamily of Sino-Tibetan) called Mahakiranti:

    Athpare
    Belhare
    Camling
    Chepang
    Dumi
    Khaling
    Kham
    Hayu
    Kulung
    Limbu
    Magar
    Magar (Syangja)
    Newar (Dolakha)
    Newari (Kathmandu)
    Thangmi
    Thulung
    Wambule
    Yamphu
    """
    update_classification(
        session, timestamp,
        'ath bel cml cpn dmi khg kmh hay klg lim mag msy nwd new thn thu wme ybi'.split(),
        'mahakiranti', genus_name='Mahakiranti', family_id='sinotibetan', subfamily='Tibeto-Burman')


def issue16(session, timestamp):
    """
    (1) Greater Central Philippine;
    (2) Northern Luzon;
    (3) Central Luzon;
    (4) Batanic; and
    (5) Bilic.
    """
    def lgs(genus):
        return [l.id for l in models.Genus.get(genus, session=session).languages]

    ruk = common.Language.get('ruk', session=session)
    ruk.name = 'Rukai (Tanan)'
    ruk.ascii_name == 'rukai tanan'

    for args, kw in [
        (('akl bat bkl ceb hnn hil mmn tag tgb tsg wwy bkd kuz mgn mwb mrn agc agd grt mgd'.split(), 'greatercentralphilippine'),
            dict(genus_name='Greater Central Philippine')),
        (('bgz'.split(), 'barito'),
            dict()),
        (('blg btk dca ibn ifu ilo isn itw kky kao pnn'.split(), 'northernluzon'),
            dict(genus_name='Northern Luzon')),
        (('kpm'.split(), 'centralluzon'),
            dict(genus_name='Central Luzon')),
        (('iva ivs ymi'.split(), 'batanic'),
            dict(genus_name='Batanic')),
        (('biq tbo try'.split(), 'bilic'),
            dict(genus_name='Bilic')),
        # A new genus called North Borneo, which involves the merger of the following two genera:
        # Kayan-Murik
        # Northwest Malayo-Polynesian
        ((lgs('kayanmurik') + lgs('northwestmalayopolynesian'), 'northborneo'),
            dict(genus_name='North Borneo')),
        # A new genus called Malayo-Sumbawan, which involves the merger of the following four genera:
        # Madurese
        # Malayic
        # Bali-Sasak
        # Sundanese
        ((lgs('madurese') + lgs('malayic') + lgs('balisasak') + lgs('sundanese'), 'malayosumbawan'),
            dict(genus_name='Malayo-Sumbawan')),

        ((['eno'], 'enggano'),
            dict(genus_name='Enggano')),
        # A new genus called Northwest Sumatra-Barrier Islands, which results from the merger of the following two genera
        # Sumatra - eno
        # Gayo
        ((filter(lambda l: l != 'eno', lgs('sumatra')) + lgs('gayo'), 'northwestsumatrabarrierislands'),
            dict(genus_name='Northwest Sumatra-Barrier Islands')),

        (([ruk], 'rukai'),
            dict(genus_name='Rukai')),

        #Minahasan genus
        #    Tondano tno
        #    Tontemboan tnt
        (('tno tnt'.split(), 'minahasan'),
            dict(genus_name='Minahasan')),

        #Sangiric genus
        #    Bantik bnt
        #    Sangir sgr
        #    Talaud tld
        #    Toratán tor
        (('bnt sgr tld tor'.split(), 'sangiric'),
            dict(genus_name='Sangiric')),

        #South Sulawesi genus
        #    Aralle-Tabulahan atb
        #    Bambam bbm
        #    Bugis bug
        #    Embaloh eml
        #    Konjo kjo
        #    Makassar mks
        #    Mamasa mms
        #    Mandar mnr
        #    Selayar sly
        #    Toraja trd
        (('atb bbm bug eml kjo mks mms mnr sly trd'.split(), 'southsulawesi'),
            dict(genus_name='South Sulawesi')),

        #Celebic genus
        #    Balantak blk
        #    Banggai bgg
        #    Da'a daa
        #    Kaili kli
        #    Lauje lje
        #    Muna mna
        #    Napu npu
        #    Padoe pad
        #    Pamona pna
        #    Tukang Besi tuk
        #    Uma uma
        #    Wolio wlo
        (('blk bgg daa kli lje mna npu pad pna tuk uma wlo'.split(), 'celebic'),
            dict(genus_name='Celebic')),

    ]:
        kw.setdefault('family_id', 'austronesian')
        update_classification(session, timestamp, *args, **kw)

    for genus, new in {
        'mesophilippine': None,
        'northernphilippines': None,
        'southmindanao': 'bilic',
        'southernphilippines': None,
        'kayanmurik': 'northborneo',
        'northwestmalayopolynesian': 'northborneo',

        'madurese': 'malayosumbawan',
        'malayic': 'malayosumbawan',
        'balisasak': 'malayosumbawan',
        'sundanese': 'malayosumbawan',

        'sumatra': 'northwestsumatrabarrierislands',
        'gayo': 'northwestsumatrabarrierislands',
        'sulawesi': None,
    }.items():
        delete(session, models.Genus.get(genus, session=session), replacement=new)


def issue17(session, timestamp):
    """
    The language Moraori (wals code mri) should be taken out of the Morehead and Upper
    Maro Rivers family and placed in a new family and new genus both called Moraori.
    """
    update_classification(
        session, timestamp,
        ['mri'],
        'moraori', genus_name='Moraori', family_id='moraori', family_name='Moraori')


def issue19(session, timestamp):
    """
    First, the following two languages currently classified as Arawakan need to be removed
    and each put in their own families where the name of the family and the genus is the
    same as the name of the language

    Aikaná aik
    Iranxe irx

    The remaining Arawakan languages need to be split into separate genera as follows:

    Northern Arawakan
        Achagua acg
        Arawak ara
        Bahuana bah
        Baniwa bnw
        Baré bae
        Curripaco cur
        Garifuna grf
        Goajiro goa
        Maipure mpr
        Piapoco ppc
        Resígaro res
        Tariana tar
        Wapishana wps
        Warekena wrk
        Yucun ycn

    Western Arawakan
        Amuesha amu

    Central Arawakan
        Parecis prc
        Waurá wur

    Eastern Arawakan
        Palikur plk

    Purus
        Apuriña apu
        Piro pir

    Bolivia-Parana
        Baure baq
        Ignaciano ign
        Terêna trn

    Pre-Andine Arawakan
        Campa (Axininca) cax
        Campa Pajonal Asheninca cpa
        Machiguenga mch
        Nomatsiguenga nom
    """
    for args, kw in [
        ((['aik'], 'aikana'),
            dict(genus_name='Aikaná', family_id='aikana', family_name='Aikaná')),
        ((['irx'], 'iranxe'),
            dict(genus_name='Iranxe', family_id='iranxe', family_name='Iranxe')),
        (('acg ara bah bnw bae cur grf goa mpr ppc res tar wps wrk ycn'.split(), 'northernarawakan'),
            dict(genus_name='Northern Arawakan')),
        (('amu'.split(), 'westernarawakan'),
            dict(genus_name='Western Arawakan')),
        (('prc wur'.split(), 'centralarawakan'),
            dict(genus_name='Central Arawakan')),
        (('plk'.split(), 'easternarawakan'),
            dict(genus_name='Eastern Arawakan')),
        (('apu pir'.split(), 'purus'),
            dict(genus_name='Purus')),
        (('baq ign trn'.split(), 'boliviaparana'),
            dict(genus_name='Bolivia-Parana')),
        (('cax cpa mch nom'.split(), 'preandinearawakan'),
            dict(genus_name='Pre-Andine Arawakan')),
    ]:
        kw.setdefault('family_id', 'arawakan')
        update_classification(session, timestamp, *args, **kw)

    delete(session, models.Genus.get('arawakan', session=session))


def issue0(session, timestamp):
    for i in session.query(common.Identifier)\
            .filter(common.Identifier.name == 'Bembe (CK if same Bembe)'):
        i.name = 'Bembe'


def issue20(session, timestamp):
    #    Datapoint http://wals.info/datapoint/121A/wals_code_bej should be changed to be
    # about Kemant (wals_code_kem). The same applies to the Rossini source for that
    # datapoint. (This is the only datapoint for this source.)
    vs_switch_lang(session, timestamp, '121A-bej', 'kem')

    #    Eastern Ojibwa (wals_code_oji) should link to two ISO codes, ojg (as it is now) but also otw.
    update_iso(session, timestamp, 'oji', otw='Ottawa')

    #    There should be two ISO codes for Campa (Axininca) (wals_code_cax): cni and cpc
    update_iso(session, timestamp, 'cax', cpc='Ajyíninka Apurucayali')

    #    All of the datapoints for Fula (Nigerian) (wals_code_fni) based on Arnott (1970)
    # need to be moved to Fula (Cameroonian) (wals_code_fua). In some cases, this involves
    # merging these datapoints with existing datapoints for wals_code_fua.
    source = common.Source.get('Arnott-1970', session=session)
    for vsr in source.valuesetreferences:
        vs = vsr.valueset
        if vs.language.id == 'fni':
            vs_switch_lang(session, timestamp, vs, 'fua')

    #    The one datapoint for Fulani (Gombe) fgo needs to be moved to Fula (Cameroonian)
    # (wals_code_fua), thus removing Fulani (Gombe) as a language.
    vs_switch_lang(session, timestamp, '27A-fgo', 'fua')

    #    Tlapanec (wals_code_tlp) should link to ISO code tcf rather than tpx.
    update_iso(session, timestamp, 'tlp', 'tpx', tcf="Malinaltepec Me'phaa")

    #    Kongo (wals_code_kon) should link to two ISO codes, kwy and kng.
    update_iso(session, timestamp, 'kon', kwy=None)

    #    One of the sources for Vili (wals_code_vif), namely Carrie (1890) turns out not
    # to be a source for Vili but another source for Kongo (wals_code_kon). This means:
    #    the page numbers given for Vili for 81A and 82A should be added to the corresponding
    #    datapoints for Kongo
    #    the value and source given for Vili for 91A should be transferred to Congo (which
    #    currently does not have a value for that feature)
    #    all the datapoints for Vili for which Carrie was the source should be removed
    #    the values given for Vili for which Carrie was the source for the features
    #    associated with chapters 112, 143, and 144 are NOT being transferred to Kongo
    #    since they are inconsistent with the existing values for these features for Kongo
    source = common.Source.get('Carrie-1890', session=session)
    for vsr in source.valuesetreferences:
        vs = vsr.valueset
        if vs.language.id == 'vif':
            if vs.parameter.id in ['81A', '82A', '91A']:
                vs_switch_lang(session, timestamp, vs, 'kon')
            else:
                vs_delete(session, timestamp, vs)

    #    One of the sources for Chichewa (wals_code_cic), namely Mateene 1980, turns out
    #    to be a source for Nyanga (wals_code_nng). What this entail is
    #    the values listed for Chichewa for features 81A, 82A, 83A, 86A, 87A, and 88A,
    #    need to be added to Nyanga
    #    Mateene 1980 should be added as a source for Nyanga
    #    the references to Mateene as a source for datapoints for Chichewa need to be removed
    #    there is one datapoint for Chichewa were Mateene is listed as the only source,
    #    namely for 83A, but this is an error: the source for this datapoint should be
    #    Price 1966: passim; Mchombo 2004: 19 (the sources listed for 81A)
    source = common.Source.get('Mateene-1980', session=session)
    for vsr in source.valuesetreferences:
        vs = vsr.valueset
        if vs.language.id == 'cic':
            if vs.parameter.id in ['81A', '82A', '83A', '86A', '87A', '88A']:
                vs_copy_lang(session, timestamp, vs, 'nng')
            else:
                vs_delete(session, timestamp, vs)
            session.delete(vsr)
            if vs.parameter.id == '83A':
                session.add(common.ValueSetReference(
                    valueset=vs,
                    source=common.Source.get('Price-1966', session=session),
                    description='passim'))
                session.add(common.ValueSetReference(
                    valueset=vs,
                    source=common.Source.get('Mchombo-2004', session=session),
                    description='19'))

    #    [gby] should be removed as an ISO code for Gwari (wals_code_gwa); the only one should be [gbr]
    update_iso(session, timestamp, 'gwa', 'gby', gbr=None)

    #    The ISO code for Grebo (wals_code_grb) should be corrected to [grj].
    update_iso(session, timestamp, 'grb', 'gry', grj="Southern Grebo")

    #    The only ISO code for Lega is [lea]; please remove the second one.
    update_iso(session, timestamp, 'leg', 'lgm')

    #    The sources for Ngbaka (wals_code_ngb) are actually for two different, only
    #    distantly related languages. GrandEury is the source for Ngbaka (Minagende), which
    #    has the same ISO code [nga] and location we are currently using for Ngbaka, so we
    #    should keep the WALS code for that Ngbaka (but should change the name to
    #    Ngbaka (Minagende)). Thomas (1963) is a source for what will be a new WALS language,
    #    Ngbaka (Ma’bo). Its ISO code is [nbm]. We could use the same code nbm as the WALS code.
    #    It belongs to the Ubangi genus, as Ngbaka (Minagende) does in the current WALS
    #    classification, but see below where Ngbaka (Minagende) is being moved out of
    #    Ubangi into a new genus. I would use the Glottolog location for it, but I can’t find
    #    that in the new Glottolog. It is also in the Democratic Republic of the Congo.
    #
    #    This means that all the datapoints in the current WALS that use Thomas 1963 as a
    #    source for Ngbaka need to be moved or copied to the new Ngbaka (Ma’bo). Those
    #    datapoints in the current Ngbaka that only use Thomas as a source will need to be
    #    removed (since that language is the new Ngbaka (Minagende)). Those datapoints that
    #    use both sources in the current WALS will now become two datapoints, one for each
    #    of these two languages.
    nbm = models.WalsLanguage(
        id='nbm',
        name="Ngbaka (Ma'bo)",
        ascii_name=slug("Ngbaka (Ma'bo)"),
        latitude=3.56,
        longitude=18.36,
        genus=models.Genus.get('ubangi', session=session))
    nbm.countries.append(models.Country.get('CD', session=session))
    session.add(nbm)
    update_iso(session, timestamp, nbm, nbm="Ngbaka Ma'bo")
    update_glottocode(session, timestamp, nbm, 'ngba1284')

    ngb = common.Language.get('ngb', session=session)
    ngb.name = 'Ngbaka (Minagende)'
    ngb.ascii_name = slug(ngb.name)

    for vs in ngb.valuesets:
        if 'Thomas-1963' in [ref.source.id for ref in vs.references]:
            if len(vs.references) > 1:
                vs_copy_lang(session, timestamp, vs, nbm)
            else:
                vs_switch_lang(session, timestamp, vs, nbm)

    #    The ISO code for Sisaala (wals_code_ssa) needs to be changed from [ssl] to [sld].
    update_iso(session, timestamp, 'ssa', 'ssl', sld='Sissala')

    #    The ISO code for Makua (wals_code_mua) should be changed to [mgh] and [xsq].
    update_iso(session, timestamp, 'mua', 'vmw', mgh='Makhuwa-Meetto', xsq='Makhuwa-Saka')

    #    A change to the genealogical classification: Four languages need to be taken out
    #    of the Ubangi genus and put into a new genus within Niger-Congo called
    #    Gbaya-Manza-Ngbaka: (first below is WALS code, last is ISO code):
    #
    #gbb Gbeya Bossangoa gbp
    #gbk Gbaya Kara gya
    #mdo Mbodomo gmm
    #ngb Ngbaka nga
    #
    update_classification(
        session, timestamp,
        ['gbb', 'gbk', 'mdo', 'ngb'],
        'gbayamanzangbaka',
        genus_name='Gbaya-Manza-Ngbaka',
        family_id='nigercongo')


def issue27(session, timestamp):
    merge_sources(session, timestamp, 'Ming-Chao-Gui-2000', 'Gui-2000')


def issue28(session, timestamp):
    merge_sources(session, timestamp, 'Lamwamu-1973', 'Lumwamu-1973', 'series', 'volume')


def issue26(session, timestamp):
    for lid, gid in [('rji', 'bodic'), ('moc', 'northomotic'), ('awk', 'kainji')]:
        update_classification(session, timestamp, [lid], gid)


def issue24(session, timestamp):
    #- Update language cea (name, coords, alternative names, iso code (and name))
    #Change name of Cree (Eastern) to Cree (Swampy)
    #Change coordinates to 56dN, 90dW
    #Change the Ethnologue name to Cree (Swampy)
    #Remove the Routledge and Other names
    #Change the ISO code to csw. glottocode to swam1239
    cea = common.Language.get('cea', session=session)
    cre = common.Language.get('cre', session=session)

    for i in range(len(cea.languageidentifier)):
        try:
            del cea.languageidentifier[i]
        except IndexError:
            pass

    for values in [
        ('gc-csw', 'swam1239', 'Swampy Cree', 'glottolog'),
        ('csw', 'csw', 'Cree (Swampy)', 'iso639-3'),
        ('ethnologue-csw', 'Cree (Swampy)', 'ethnologue', 'name'),
    ]:
        id = common.Identifier(**dict(zip('id name description type'.split(), values)))
        cea.languageidentifier.append(common.LanguageIdentifier(language=cea, identifier=id))

    cea.updated = timestamp
    cea.name = 'Cree (Swampy)'
    cea.ascii_name = slug('Cree (Swampy)')
    cea.latitude = 56.0
    cea.longitude = -90.0

    for pid in ['81A', '82A', '83A']:
        vsq = session.query(common.ValueSet)\
            .join(common.Parameter)\
            .filter(common.Parameter.id == pid)
        vs1 = vsq.filter(common.ValueSet.language_pk == cea.pk).one()
        vs2 = vsq.filter(common.ValueSet.language_pk == cre.pk).one()
        vs2.updated = timestamp
        vs1.updated = timestamp

        for ref in vs1.references:
            if ref.source.id == 'Hive-1948':
                ref.valueset = vs2

    session.flush()


    #- Delete valueset 85A-cea
    vs = session.query(common.ValueSet)\
        .join(common.Parameter)\
        .filter(common.Parameter.id == '85A')\
        .filter(common.ValueSet.language_pk == cea.pk).one()

    session.delete(vs.values[0])
    session.delete(vs.references[0])
    session.delete(vs)

    #- delete valueset 131A-cea add 131A-cre
    vs_switch_lang(session, timestamp, '131A-cea', 'cre')
