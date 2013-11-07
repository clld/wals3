from sqlalchemy.orm import joinedload, joinedload_all

from clld.web.adapters.geojson import (
    GeoJsonParameter, GeoJsonLanguages, pacific_centered_coordinates,
)
from clld.db.meta import DBSession
from clld.db.models.common import Value, DomainElement, ValueSet


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
