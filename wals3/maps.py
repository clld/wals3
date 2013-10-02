from clld.web.maps import ParameterMap, Map, Layer
from clld.web.adapters import GeoJsonLanguages
from clld.web.util.helpers import JS


class FeatureMap(ParameterMap):
    def options(self):
        return {
            'icon_size': 20,
            'worldCopyJump': True,
            'on_init': JS('wals_parameter_map_on_init'),
            'info_query': {'parameter': self.ctx.pk}}


class _GeoJson(GeoJsonLanguages):
    def feature_iterator(self, ctx, req):
        for language in ctx.languages:
            yield language


class FamilyMap(Map):
    def get_layers(self):
        geojson = _GeoJson(self.ctx)
        for genus in self.ctx.genera:
            yield Layer(
                genus.id,
                genus.name,
                geojson.render(genus, self.req, dump=False))


class CountryMap(Map):
    def get_layers(self):
        geojson = _GeoJson(self.ctx)
        yield Layer(
            self.ctx.id, self.ctx.name, geojson.render(self.ctx, self.req, dump=False))


class SampleMap(Map):
    def get_layers(self):
        geojson = _GeoJson(self.ctx)
        yield Layer('sample', 'Sample', geojson.render(self.ctx, self.req, dump=False))
