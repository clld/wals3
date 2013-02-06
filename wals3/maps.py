from clld.web.maps import ParameterMap, Map
from clld.web.util.htmllib import HTML
from clld.web.adapters import GeoJsonLanguages


class FeatureMap(ParameterMap):
    def get_layers(self):
        res = []
        for layer, de in zip(ParameterMap.get_layers(self), self.ctx.domain):
            layer['marker'] = HTML.img(src=self.req.static_url('wals3:static/icons/' + de.icon_id + '.png'))
            res.append(layer)
        return res

    def options(self):
        return {'style_map': 'wals_feature', 'info_query': {'parameter': self.ctx.pk}}


class _GeoJson(GeoJsonLanguages):
    def feature_iterator(self, ctx, req):
        for genus in ctx.genera:
            for language in genus.languages:
                yield language


class FamilyMap(Map):
    def get_layers(self):
        geojson = _GeoJson(self.ctx)
        return [{
            'name': self.ctx.name,
            'data': geojson.render(self.ctx, self.req, dump=False),
        }]
