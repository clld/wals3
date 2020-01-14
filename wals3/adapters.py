from itertools import groupby

from sqlalchemy.orm import joinedload, subqueryload

from clldutils.misc import lazyproperty
from clld.interfaces import ILanguage, IParameter, IIndex, ICldfConfig
from clld.web.adapters.base import Index
from clld.web.adapters.cldf import CldfConfig
from clld.web.adapters.geojson import GeoJsonParameter, GeoJson
from clld.web.adapters.download import CsvDump
from clld.web.maps import SelectedLanguagesMap, Layer
from clld.web.util.helpers import map_marker_img
from clld.db.meta import DBSession
from clld.db.models.common import (
    Value, DomainElement, ValueSet, Language, Parameter, LanguageIdentifier,
)

from wals3.models import WalsLanguage, Genus


class GeoJsonFeature(GeoJsonParameter):
    def feature_iterator(self, ctx, req):
        return DBSession.query(Value).join(DomainElement)\
            .filter(DomainElement.id == req.params.get('domainelement'))\
            .options(
                joinedload(Value.valueset).joinedload(ValueSet.language),
                joinedload(Value.domainelement))

    def get_language(self, ctx, req, value):
        return value.valueset.language

    def feature_properties(self, ctx, req, value):
        return {
            'value_numeric': value.domainelement.number,
            'value_name': value.domainelement.name}


class GeoJsonLects(GeoJson):
    def feature_properties(self, ctx, req, language):
        if hasattr(ctx, 'icon_url'):  # pragma: no cover
            # special handling for domain elements of feature combinations
            return {'icon': ctx.icon_url}


class Matrix(CsvDump):
    md_fields = [
        ('wals_code', lambda p: p.id),
        ('iso_code', lambda p: p.iso_code),
        ('glottocode', lambda p: p.glottocode),
        ('Name', lambda p: p.name),
        ('latitude', lambda p: p.latitude),
        ('longitude', lambda p: p.longitude),
        ('genus', lambda p: p.genus.name),
        ('family', lambda p: p.genus.family.name),
        ('macroarea', lambda p: p.macroarea),
        ('countrycodes', lambda p: ' '.join(c.id for c in p.countries)),
    ]
    _fields = []

    @lazyproperty
    def _parameters(self):
        return DBSession.query(Parameter).order_by(Parameter.pk).all()

    def query(self, req):
        self._domainelements = DBSession.query(DomainElement).all()
        return DBSession.query(Language)\
            .order_by(Language.id)\
            .options(
                subqueryload('languageidentifier').subqueryload('identifier'),
                subqueryload('countries'),
                joinedload(Language.valuesets).joinedload(ValueSet.values),
                joinedload(WalsLanguage.genus).joinedload(Genus.family))

    def get_fields(self, req):  # pragma: no cover
        if not self._fields:
            self._fields = [f[0] for f in self.md_fields]
            self._fields.extend(['{0.id} {0.name}'.format(p) for p in self._parameters])
        return self._fields

    def row(self, req, fp, item, index):  # pragma: no cover
        values = {
            '{0.id} {0.name}'.format(v.parameter):
            '{0.number} {0.name}'.format(v.values[0].domainelement)
            for v in item.valuesets}
        for name, getter in self.md_fields:
            value = getter(item)
            values[name] = value if value is not None else ''
        values['URL'] = req.resource_url(item)
        return [values.get(p, '') for p in self.get_fields(req)]


class _SelectedLanguagesMap(SelectedLanguagesMap):
    def get_layers(self):
        for genus, languages in groupby(
                sorted(self.languages, key=lambda l: l.genus_pk), key=lambda l: l.genus):
            languages = list(languages)
            yield Layer(
                genus.id,
                genus.name,
                self.geojson_impl(languages).render(self.ctx, self.req, dump=False),
                marker=map_marker_img(self.req, genus),
                representation=len(languages))


class MapView(Index):
    extension = str('map.html')
    mimetype = str('text/vnd.clld.map+html')
    send_mimetype = str('text/html')
    template = 'language/map_html.mako'

    def template_context(self, ctx, req):
        langs = list(ctx.get_query(limit=8000))
        return {'map': _SelectedLanguagesMap(ctx, req, langs), 'languages': langs}


class LanguagesTab(Index):
    extension = str('tab')
    mimetype = str('text/vnd.clld.text+tsv')
    send_mimetype = str('text/plain')

    def render(self, ctx, req):
        fields = [
            ('wals code', lambda l: l.id),
            ('glottocode', lambda l: l.glottocode),
            ('name', lambda l: l.name),
            ('latitude', lambda l: l.latitude),
            ('longitude', lambda l: l.longitude),
            ('macroarea', lambda l: l.macroarea),
            ('genus', lambda l: l.genus.name),
            ('family', lambda l: l.genus.family.name),
            ('sample 100', lambda l: l.samples_100),
            ('sample 200', lambda l: l.samples_200),
        ]
        lines = [[f[0] for f in fields]]
        for lang in DBSession.query(Language).options(
            joinedload(WalsLanguage.genus).joinedload(Genus.family),
            joinedload(Language.languageidentifier).joinedload(LanguageIdentifier.identifier)
        ):
            lines.append([f[1](lang) for f in fields])
        return '\n'.join('\t'.join(['%s' % l for l in line]) for line in lines)


class WalsCldfConfig(CldfConfig):
    module = 'StructureDataset'

    def custom_schema(self, req, ds):
        ds.add_columns('LanguageTable', 'Genus')

    def query(self, model):
        q = CldfConfig.query(self, model)
        if model == Language:
            q = q.options(joinedload(WalsLanguage.genus))
        return q

    def convert(self, model, item, req):
        res = CldfConfig.convert(self, model, item, req)
        if model == Language:
            res.update(Genus=item.genus.name)
        return res


def includeme(config):
    config.registry.registerUtility(WalsCldfConfig(), ICldfConfig)
    config.register_adapter(GeoJsonFeature, IParameter)
    config.register_adapter(MapView, ILanguage, IIndex)
    config.register_adapter(LanguagesTab, ILanguage, IIndex)
