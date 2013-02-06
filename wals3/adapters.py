from sqlalchemy.orm import joinedload

from clld.web.adapters import GeoJsonParameter
from clld.db.meta import DBSession
from clld.db.models.common import Value, DomainElement


class GeoJsonFeature(GeoJsonParameter):
    def feature_iterator(self, ctx, req):
        return DBSession.query(Value).join(DomainElement)\
            .filter(DomainElement.id == req.params.get('domainelement'))\
            .options(joinedload(Value.language), joinedload(Value.domainelement))

    def feature_coordinates(self, ctx, req, value):
        return [value.language.longitude, value.language.latitude]

    def feature_properties(self, ctx, req, value):
        language = value.language
        return {
            'name': language.name,
            'id': language.id,
            'icon_type': value.domainelement.icon_id[:1],
            'icon_color': '#%s' % ''.join(2 * c for c in value.domainelement.icon_id[1:]),
            'value_numeric': value.domainelement.numeric,
            'value_name': value.domainelement.name}
