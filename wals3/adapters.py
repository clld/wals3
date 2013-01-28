from clld.web.adapters import GeoJsonParameter


class GeoJsonFeature(GeoJsonParameter):

    def feature_properties(self, ctx, req, feature):
        language, values = feature
        val = list(values)[0]
        if val.domainelement.id == req.params.get('domainelement'):
            res = GeoJsonParameter.feature_properties(self, ctx, req, feature)
            res['icon_type'] = val.domainelement.icon_id[:1]
            res['icon_color'] = '#%s' % ''.join(2*c for c in val.domainelement.icon_id[1:])
            res['value_numeric'] = val.domainelement.numeric
            res['value_name'] = val.domainelement.name
            return res
