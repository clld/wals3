from clld.db.models.common import Identifier, LanguageIdentifier, Language, IdentifierType
from clld.db.migration import Connection as BaseConnection

from wals3.models import Family, Genus, WalsLanguage


class Connection(BaseConnection):
    def insert_if_missing(self, model, where, values=None):
        values = values or {}
        row = self.first(model, **where)
        if row:
            return row.pk
        values.update(where)
        return self.insert(model, **values)

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
            elif isinstance(family, basestring):
                family = self.pk(Family, family)

        if isinstance(genus, (tuple, list)):
            assert family
            genus = self.insert(Genus, id=genus[0], name=genus[1], family_pk=family)
        elif isinstance(genus, basestring):
            genus = self.pk(Genus, genus)

        self.update(WalsLanguage, dict(genus_pk=genus), pk=lpk)
