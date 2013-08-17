from sqlalchemy.orm import joinedload, joinedload_all

from clld.web.adapters import GeoJsonParameter
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

    def feature_properties(self, ctx, req, value):
        return {
            'icon_type': value.domainelement.jsondata['icon'][:1],
            'icon_color': '#%s' % ''.join(2 * c for c in value.domainelement.jsondata['icon'][1:]),
            'value_numeric': value.domainelement.number,
            'value_name': value.domainelement.name}
