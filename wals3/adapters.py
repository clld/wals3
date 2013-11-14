from __future__ import unicode_literals

from sqlalchemy.orm import joinedload, joinedload_all, contains_eager

from clld.web.adapters.geojson import (
    GeoJsonParameter, GeoJsonLanguages, pacific_centered_coordinates,
)
from clld.web.adapters.download import CsvDump
from clld.db.meta import DBSession
from clld.db.models.common import Value, DomainElement, ValueSet, Language, Parameter
from wals3.models import WalsLanguage, Genus


class GeoJsonFeature(GeoJsonParameter):
    def feature_iterator(self, ctx, req):
        return DBSession.query(Value).join(DomainElement)\
            .filter(DomainElement.id == req.params.get('domainelement'))\
            .options(
                joinedload_all(Value.valueset, ValueSet.language),
                joinedload(Value.domainelement),
            )

    def get_language(self, ctx, req, value):
        return value.valueset.language

    def get_coordinates(self, language):
        return pacific_centered_coordinates(language)

    def feature_properties(self, ctx, req, value):
        return {
            'value_numeric': value.domainelement.number,
            'value_name': value.domainelement.name}


class GeoJsonLects(GeoJsonLanguages):
    def feature_iterator(self, ctx, req):
        for language in ctx.languages:
            yield language

    def get_coordinates(self, language):
        return pacific_centered_coordinates(language)


class Matrix(CsvDump):
    md_fields = [
        ('wals_code', lambda p: p.id),
        ('iso_code', lambda p: p.iso_code or ''),
        ('glottocode', lambda p: p.glottocode or ''),
        ('Name', lambda p: p.name),
        ('latitude', lambda p: p.latitude),
        ('longitude', lambda p: p.longitude),
        ('genus', lambda p: p.genus.name),
        ('family', lambda p: p.genus.family.name),
    ]
    _fields = []

    def query(self, req):
        return DBSession.query(Language)\
            .order_by(Language.id)\
            .options(
                joinedload(Language.valuesets),
                joinedload_all(WalsLanguage.genus, Genus.family))

    def get_fields(self, req):  # pragma: no cover
        if not self._fields:
            self._fields = [f[0] for f in self.md_fields]
            self._fields.extend(['{0.id} {0.name}'.format(p) for p in DBSession.query(Parameter).order_by(Parameter.pk)])
        return self._fields

    def row(self, req, fp, item, index):  # pragma: no cover
        values = {'{0.id} {0.name}'.format(v.parameter): '{0.number} {0.name}'.format(v.values[0].domainelement) for v in item.valuesets}
        for name, getter in self.md_fields:
            values[name] = getter(item) or ''
        values['URL'] = req.resource_url(item)
        return [values.get(p, '') for p in self.get_fields(req)]
