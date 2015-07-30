from clld.web.maps import ParameterMap, Map, Layer, CombinationMap
from clld.web.util.helpers import JS, map_marker_img

from wals3.adapters import GeoJsonLects


class FeatureMap(ParameterMap):
    def get_options(self):
        return {
            'icon_size': 20,
            'max_zoom': 9,
            'worldCopyJump': True,
            'on_init': JS('wals_parameter_map_on_init'),
            'info_query': {'parameter': self.ctx.pk}}


class WalsMap(Map):
    def get_options(self):
        return {'max_zoom': 9, 'show_labels': True, 'hash': True}


def get_geojson(req, obj, ctx=None):
    return GeoJsonLects(obj).render(ctx or obj, req, dump=False)


class FamilyMap(WalsMap):
    def get_layers(self):
        for genus in self.ctx.genera:
            yield Layer(
                genus.id,
                genus.name,
                get_geojson(self.req, self.ctx, genus),
                marker=map_marker_img(self.req, genus))


class GenusMap(WalsMap):
    def get_layers(self):
        yield Layer(
            self.ctx.id,
            self.ctx.name,
            get_geojson(self.req, self.ctx),
            marker=map_marker_img(self.req, self.ctx))


class CountryMap(WalsMap):
    def get_layers(self):
        yield Layer(self.ctx.id, self.ctx.name, get_geojson(self.req, self.ctx))


class SampleMap(Map):
    def get_options(self):
        return {'icon_size': 20}

    def get_layers(self):
        yield Layer('sample', 'Sample', get_geojson(self.req, self.ctx))


class CombinedMap(CombinationMap):
    def get_options(self):
        return {'icon_size': 20, 'hash': True}


def includeme(config):
    config.register_map('parameter', FeatureMap)
    config.register_map('family', FamilyMap)
    config.register_map('genus', GenusMap)
    config.register_map('country', CountryMap)
    config.register_map('sample', SampleMap)
    config.register_map('combination', CombinedMap)
