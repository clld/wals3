from __future__ import unicode_literals

from six import string_types

from clld.db.models.common import (
    Identifier, LanguageIdentifier, Language, IdentifierType, Source,
)
from clld.db.migration import Connection as BaseConnection
from clld.util import slug

from wals3.models import Family, Genus, WalsLanguage


class Connection(BaseConnection):
    def insert_if_missing(self, model, where, values=None):
        values = values or {}
        row = self.first(model, **where)
        if row:
            return row.pk
        values.update(where)
        return self.insert(model, **values)

    def update_glottocode(self, lid, gc):
        lpk = self.pk(Language, lid)

        for li in self.select(LanguageIdentifier, language_pk=lpk):
            i = self.get(Identifier, li.identifier_pk)
            if i.type == 'glottolog':
                self.update(Identifier, dict(name=gc), pk=i.pk)
                break
        else:
            ipk = self.insert_if_missing(
                Identifier,
                dict(id=gc),
                dict(name=gc, description=gc, type='glottolog'))
            self.insert(LanguageIdentifier, identifier_pk=ipk, language_pk=lpk)

    def update_iso(self, lid, *obsolete, **new):  # pragma: no cover
        lpk = self.pk(Language, lid)

        for _code in obsolete:
            for code in [_code, 'ethnologue-' + _code]:
                i = self.pk(Identifier, code)
                li = self.first(LanguageIdentifier, identifier_pk=i, language_pk=lpk)
                if li:
                    self.delete(LanguageIdentifier, identifier_pk=li.pk, language_pk=lpk)

        for code, name in new.items():
            ipk = self.insert_if_missing(
                Identifier,
                dict(id=code),
                dict(name=code, description=name, type=IdentifierType.iso.value))
            self.insert_if_missing(
                LanguageIdentifier, dict(identifier_pk=ipk, language_pk=lpk))

            ipk = self.insert_if_missing(
                Identifier,
                dict(id='ethnologue-' + code),
                dict(name=name, description='ethnologue', type='name'))
            self.insert_if_missing(
                LanguageIdentifier, dict(identifier_pk=ipk, language_pk=lpk))
        return lpk

    def update_genus(self, lid, genus, family=None):
        lpk = self.pk(Language, lid)

        # check whether we have to create a new genus and maybe even family:
        if family:
            if isinstance(family, (tuple, list)):
                family = self.insert(Family, id=family[0], name=family[1])
            elif isinstance(family, string_types):
                family = self.pk(Family, family)

        if isinstance(genus, (tuple, list)):
            assert family
            genus = self.insert(
                Genus, id=genus[0], name=genus[1], icon=genus[2], family_pk=family)
        elif isinstance(genus, string_types):
            genus = self.pk(Genus, genus)

        self.update(WalsLanguage, dict(genus_pk=genus), pk=lpk)

    def update_name(self, lid, newname):
        lpk = self.pk(Language, lid)
        self.update(Language, dict(name=newname), pk=lpk)
        self.update(
            WalsLanguage, dict(ascii_name=slug(newname, remove_whitespace=False)), pk=lpk)

    def update_source(self, sid, **kw):
        pk = self.pk(Source, sid)
        self.update(Source, kw, pk=pk)
