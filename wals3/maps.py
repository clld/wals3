from clld.web.maps import ParameterMap, Map
from clld.web.util.htmllib import HTML


class FeatureMap(ParameterMap):
    def get_layers(self):
        res = []
        for layer, de in zip(ParameterMap.get_layers(self), self.ctx.domain):
            layer['marker'] = HTML.img(src=self.req.static_url('wals3:static/icons/' + de.icon_id + '.png'))
            res.append(layer)
        return res

    def options(self):
        return {'style_map': 'wals_feature'}
