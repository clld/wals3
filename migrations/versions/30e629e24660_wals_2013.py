# coding=utf-8
"""WALS 2013

Revision ID: 30e629e24660
Revises: 274ff6197e85
Create Date: 2013-10-31 12:06:15.203205

"""
from __future__ import unicode_literals

# revision identifiers, used by Alembic.
revision = '30e629e24660'
down_revision = '274ff6197e85'

import datetime

from alembic import op
import sqlalchemy as sa

from clld.db.migration import merge_sources, pk, insert, delete, update, select
from clld.db.models.common import (
    Language, Identifier, LanguageIdentifier, Value, ValueSet, ValueSentence,
    ValueSetReference, Source,
)
from wals3 import models


def upgrade():
    conn = op.get_bind()

    #---------------------------
    #26
    for lid, gid in [('rji', 'bodic'), ('moc', 'northomotic'), ('awk', 'kainji')]:
        lpk = pk(conn, Language, lid)
        gpk = pk(conn, models.Genus, gid)
        update(conn, models.WalsLanguage, dict(genus_pk=gpk), pk=lpk)

    #---------------------------
    #27
    merge_sources(conn, 'Ming-Chao-Gui-2000', 'Gui-2000')

    #---------------------------
    #28
    merge_sources(conn, 'Lamwamu-1973', 'Lumwamu-1973', 'series', 'volume')

    #---------------------------
    #24
    #- Update language cea (name, coords, alternative names, iso code (and name))
    #Change name of Cree (Eastern) to Cree (Swampy)
    #Change coordinates to 56dN, 90dW
    #Change the Ethnologue name to Cree (Swampy)
    #Remove the Routledge and Other names
    #Change the ISO code to csw. glottocode to swam1239
    cea = pk(conn, Language, 'cea')
    cre = pk(conn, Language, 'cre')

    delete(conn, LanguageIdentifier, language_pk=cea)
    for values in [
        ('gc-csw', 'swam1239', 'Swampy Cree', 'glottolog'),
        ('csw', 'csw', 'Cree (Swampy)', 'iso639-3'),
        ('ethnologue-csw', 'Cree (Swampy)', 'ethnologue', 'name'),
    ]:
        ipk = insert(
            conn, Identifier, **dict(zip('id name description type'.split(), values)))
        insert(conn, LanguageIdentifier, language_pk=cea, identifier_pk=ipk)

    update(
        conn, Language, dict(name='Cree (Swampy)', latitude=56.0, longitude=-90.0),
        pk=cea)

    #- Update valuesetreference from valueset 81A/82A/83A-cea -> cre
    for fid in ['81A', '82A', '83A']:
        spk = pk(conn, Source, 'Hive-1948')
        vspk1 = pk(conn, ValueSet, fid + '-cea')
        vspk2 = pk(conn, ValueSet, fid + '-cre')
        update(conn, ValueSetReference,
               dict(valueset_pk=vspk2), valueset_pk=vspk1, source_pk=spk)

    #- Delete valueset 85A-cea
    vspk = pk(conn, ValueSet, '85A-cea')
    vpk = pk(conn, Value, vspk, attr='valueset_pk')
    delete(conn, ValueSentence, value_pk=vpk)
    delete(conn, Value, pk=vpk)
    delete(conn, ValueSetReference, valueset_pk=vspk)
    delete(conn, ValueSet, pk=vspk)

    #- Update language in valueset 131A-cea
    update(conn, ValueSet, dict(language_pk=cre), id='131A-cea')

    #---------------------------
    #20
    #    Datapoint http://wals.info/datapoint/121A/wals_code_bej should be changed to be
    # about Kemant (wals_code_kem). The same applies to the Rossini source for that
    # datapoint. (This is the only datapoint for this source.)
    update(conn, ValueSet, dict(language_pk=pk(conn, Language, 'kem')), id='121A-bej')

    #    Eastern Ojibwa (wals_code_oji) should link to two ISO codes, ojg (as it is now) but also otw.
    ipk = insert(
        conn, Identifier, id='otw', name='otw', description='Ottawa', type='iso639-3')
    oji = pk(conn, Language, 'oji')
    insert(conn, LanguageIdentifier, language_pk=oji, identifier_pk=ipk)

    #    There should be two ISO codes for Campa (Axininca) (wals_code_cax): cni and cpc
    ipk = insert(
        conn, Identifier, id='cpc', name='cpc', description='Ajyíninka Apurucayali', type='iso639-3')
    cax = pk(conn, Language, 'cax')
    insert(conn, LanguageIdentifier, language_pk=cax, identifier_pk=ipk)

    #    All of the datapoints for Fula (Nigerian) (wals_code_fni) based on Arnott (1970)
    # need to be moved to Fula (Cameroonian) (wals_code_fua). In some cases, this involves
    # merging these datapoints with existing datapoints for wals_code_fua.
    spk = pk(conn, Source, 'Arnott-1970')
    fni = pk(conn, Language, 'fni')
    fua = pk(conn, Language, 'fua')
    for row in select(conn, ValueSetReference, source_pk=spk).fetchall():
        vs = select(conn, ValueSet, pk=row['valueset_pk']).fetchone()
        if vs['language_pk'] == fni:
            vsfua = select(conn, ValueSet, language_pk=fua, parameter_pk=vs['parameter_pk']).fetchone()
            if vsfua:
                #
                # TODO: merge!
                # - link the valuesetreference to vsfua
                # - delete value and valueset vs
                #
                pass
            else:
                update(conn, ValueSet, dict(language_pk=fua), pk=vs['pk'])

    #    The one datapoint for Fulani (Gombe) needs to be moved to Fula (Cameroonian)
    # (wals_code_fua), thus removing Fulani (Gombe) as a language.

    #    Tlapanec (wals_code_tlp) should link to ISO code tcf rather than tpx.
    tcf = insert(
        conn, Identifier, id='tcf', name='tcf', description="Malinaltepec Me'phaa", type='iso639-3')
    tlp = pk(conn, Language, 'tlp')
    tpx = pk(conn, Identifier, 'tpx')
    update(conn, LanguageIdentifier, dict(identifier_pk=tcf), identifier_pk=tpx, language_pk=tlp)

    #    Kongo (wals_code_kon) should link to two ISO codes, kwy and kng.
    kon = pk(conn, Language, 'kon')
    kwy = pk(conn, Identifier, 'kwy')
    insert(conn, LanguageIdentifier, language_pk=kon, identifier_pk=kwy)

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

    #    One of the sources for Chichewa (wals_code_cic), namely Mateene 1980, turns out
    #    to be a source for Nyanga (wals_code_nng). What this entail is
    #    the values listed for Chichewa for features 81A, 82A, 83A, 86A, 87A, and 88A,
    #    need to be added to Nyanga
    #    Mateene 1980 should be added as a source for Nyanga
    #    the references to Mateene as a source for datapoints for Chichewa need to be removed
    #    there is one datapoint for Chichewa were Mateene is listed as the only source,
    #    namely for 83A, but this is an error: the source for this datapoint should be
    #    Price 1966: passim; Mchombo 2004: 19 (the sources listed for 81A)

    #    [gby] should be removed as an ISO code for Gwari (wals_code_gwa); the only one should be [gbr]

    #    The ISO code for Grebo (wals_code_grb) should be corrected to [grj].

    #    The only ISO code for Lega is [lea]; please remove the second one.

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

    #    The ISO code for Sisaala (wals_code_ssa) needs to be changed from [ssl] to [sld].

    #    The ISO code for Makua (wals_code_mua) should be changed to [mgh] and [xsq].

    #Note that the various changes in ISO codes above will also entail changes to the associated Ethnologue name.

    #    A change to the genealogical classification: Four languages need to be taken out
    #    of the Ubangi genus and put into a new genus within Niger-Congo called
    #    Gbaya-Manza-Ngbaka: (first below is WALS code, last is ISO code):
    #
    #gbb Gbeya Bossangoa gbp
    #gbk Gbaya Kara gya
    #mdo Mbodomo gmm
    #ngb Ngbaka nga
    #
    #(The last one here is the one we are renaming Ngbaka (Minagende).)


    #
    # TODO: must recompute representation, language sources, ...
    #


def downgrade():
    pass
