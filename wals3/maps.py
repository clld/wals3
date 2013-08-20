from clld.web.maps import ParameterMap, Map, Layer
from clld.web.adapters import GeoJsonLanguages


class FeatureMap(ParameterMap):
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
            #'name': language.name,
            #'id': language.id,
            #'icon': language.genus.icon,
            #'icon_type': language.genus.icon_id[:1],
            #'icon_color': '#%s' % ''.join(2 * c for c in language.genus.icon_id[1:]),
        }


class _Map(Map):
    def options(self):
        return {'style_map': 'wals_feature'}


class FamilyMap(_Map):
    def get_layers(self):
        geojson = _GeoJson(self.ctx)
        for genus in self.ctx.genera:
            yield Layer(
                genus.id,
                genus.name,
                geojson.render(genus, self.req, dump=False))


class CountryMap(_Map):
    def get_layers(self):
        geojson = _GeoJson(self.ctx)
        yield Layer(
            self.ctx.id, self.ctx.name, geojson.render(self.ctx, self.req, dump=False))


class SampleMap(Map):
    def get_layers(self):
        geojson = _GeoJson(self.ctx)
        yield Layer('sample', 'Sample', geojson.render(self.ctx, self.req, dump=False))
