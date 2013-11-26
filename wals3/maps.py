from clld.web.maps import ParameterMap, Map, Layer
from clld.web.util.helpers import JS, map_marker_img
from clld.web.util.htmllib import HTML

from wals3.adapters import GeoJsonLects


def map_params(req):
    res = {}
    try:
        if 'lat' in req.params and 'lng' in req.params:
            res['center'] = map(float, [req.params['lat'], req.params['lng']])
        if 'z' in req.params:
            res['zoom'] = int(req.params['z'])
    except (ValueError, TypeError):
        pass
    return res


class FeatureMap(ParameterMap):
    def get_options(self):
        res = {
            'icon_size': 20,
            'max_zoom': 9,
            'worldCopyJump': True,
            'on_init': JS('wals_parameter_map_on_init'),
            'info_query': {'parameter': self.ctx.pk}}
        res.update(map_params(self.req))
        return res


class WalsMap(Map):
    def get_options(self):
        res = {'max_zoom': 9, 'show_labels': True}
        res.update(map_params(self.req))
        return res


class FamilyMap(WalsMap):
    def get_layers(self):
        geojson = GeoJsonLects(self.ctx)
        for genus in self.ctx.genera:
            yield Layer(
                genus.id,
                genus.name,
                geojson.render(genus, self.req, dump=False),
                marker=map_marker_img(self.req, genus))


class GenusMap(WalsMap):
    def get_layers(self):
        geojson = GeoJsonLects(self.ctx)
        yield Layer(
            self.ctx.id,
            self.ctx.name,
            geojson.render(self.ctx, self.req, dump=False),
            marker=map_marker_img(self.req, self.ctx))


class CountryMap(WalsMap):
    def get_layers(self):
        geojson = GeoJsonLects(self.ctx)
        yield Layer(
            self.ctx.id, self.ctx.name, geojson.render(self.ctx, self.req, dump=False))


class SampleMap(Map):
    def get_layers(self):
        geojson = GeoJsonLects(self.ctx)
        yield Layer('sample', 'Sample', geojson.render(self.ctx, self.req, dump=False))


class CombinedMap(Map):
    def get_layers(self):
        for id_ in sorted(self.ctx.keys()):
            de = self.ctx[id_]
            if de.languages:
                geojson = GeoJsonLects(de)
                yield Layer(
                    '-'.join(map(str, de.id)),
                    de.name,
                    geojson.render(de, self.req, dump=False),
                    marker=HTML.img(src=de.icon_url, height='20', width='20'))

    def get_options(self):
        res = {'icon_size': 20, 'hash': True}
        res.update(map_params(self.req))
        return res


def includeme(config):
    config.register_map('parameter', FeatureMap)
    config.register_map('family', FamilyMap)
    config.register_map('genus', GenusMap)
    config.register_map('country', CountryMap)
    config.register_map('sample', SampleMap)
