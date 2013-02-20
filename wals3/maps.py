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
    #
    # TODO: cycle through icons to use for genera
    #
    def feature_iterator(self, ctx, req):
        for language in ctx.languages:
            yield language

    def feature_properties(self, ctx, req, language):
        return {
            'name': language.name,
            'id': language.id,
            'icon_type': language.genus.icon_id[:1],
            'icon_color': '#%s' % ''.join(2 * c for c in language.genus.icon_id[1:]),
        }


class _Map(Map):
    def options(self):
        return {'style_map': 'wals_feature'}


class FamilyMap(_Map):
    def get_layers(self):
        geojson = _GeoJson(self.ctx)
        return [{'name': genus.name, 'data': geojson.render(genus, self.req, dump=False)}
                for genus in self.ctx.genera]


class CountryMap(_Map):
    def get_layers(self):
        geojson = _GeoJson(self.ctx)
        return [{'name': self.ctx.name, 'data': geojson.render(self.ctx, self.req, dump=False)}]


class SampleMap(Map):
    def get_layers(self):
        geojson = _GeoJson(self.ctx)
        return [{'name': '100 Sample', 'data': geojson.render(self.ctx, self.req, dump=False)}]
