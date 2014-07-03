from sqlalchemy.orm import joinedload, joinedload_all
from sqlalchemy.sql.expression import cast
from sqlalchemy.types import Integer

from clld.web import datatables
from clld.web.datatables.base import (
    Col, filter_number, LinkCol, DetailsRowLinkCol, IdCol,
)
from clld.web.datatables.value import ValueNameCol
from clld.db.meta import DBSession
from clld.db.models import common
from clld.db.util import get_distinct_values, icontains
from clld.web.util.helpers import linked_contributors, link, button, icon
from clld.web.util.htmllib import HTML

from wals3.models import WalsLanguage, Genus, Family, Chapter, Feature, Area, Country
from wals3.util import comment_button


class FeatureIdCol(LinkCol):
    def get_attrs(self, item):
        return {'label': item.id}

    def order(self):
        return Feature.contribution_pk, Feature.ordinal_qualifier


class FeatureIdCol2(FeatureIdCol):
    def get_attrs(self, item):
        return {'label': item.valueset.parameter.id}

    def get_obj(self, item):
        return item.valueset.parameter


class AreaCol(Col):
    def format(self, item):
        return item.valueset.parameter.chapter.area.name

    def order(self):
        return Area.name

    def search(self, qs):
        return Area.name.contains(qs)


class _WalsValueNameCol(ValueNameCol):
    def order(self):
        return common.DomainElement.name

    def search(self, qs):
        return icontains(common.DomainElement.name, qs)


class CommentCol(Col):
    __kw__ = {'bSortable': False, 'bSearchable': False, 'sTitle': ''}

    def format(self, item):
        l = self.dt.language or item.valueset.language
        f = self.dt.parameter or item.valueset.parameter
        return comment_button(
            self.dt.req, f, l, class_='btn-mini' if self.dt.language else '')


class Datapoints(datatables.Values):
    def base_query(self, query):
        query = super(Datapoints, self).base_query(query)
        if self.language:
            query = query.join(Feature, Feature.pk == common.ValueSet.parameter_pk)\
                .join(Chapter, Area)\
                .join(common.DomainElement,
                      common.Value.domainelement_pk == common.DomainElement.pk).options(
                    joinedload(common.Value.domainelement),
                    joinedload(common.Value.valueset, common.ValueSet.parameter))
        if self.parameter:
            query = query.options(
                joinedload(common.Value.valueset, common.ValueSet.language))
        return query

    def col_defs(self):
        # remove the details link.
        cols = super(Datapoints, self).col_defs()[1:]
        if self.language:
            cols = [
                FeatureIdCol2(self, 'fid', sClass='right', bSearchable=False),
                _WalsValueNameCol(self, 'value'),
            ] + cols[1:] + [AreaCol(self, 'area', bSearchable=False)]
        cols.append(CommentCol(self, 'c'))
        return cols

    def get_options(self):
        if self.language:
            # if the table is restricted to the values for one language, the number of
            # features is an upper bound for the number of values; thus, we do not
            # paginate.
            return {'bLengthChange': False, 'bPaginate': False}


class ContributorsCol(Col):
    def format(self, item):
        return linked_contributors(self.dt.req, item.chapter)


class _AreaCol(Col):
    def __init__(self, *args, **kw):
        super(_AreaCol, self).__init__(*args, **kw)
        self.choices = [a.name for a in DBSession.query(Area).order_by(Area.id)]

    def order(self):
        return Area.name

    def search(self, qs):
        return Area.name.__eq__(qs)


class FeatureAreaCol(_AreaCol):
    def format(self, item):
        return item.chapter.area.name


class Features(datatables.Parameters):
    def base_query(self, query):
        return query.join(Chapter).join(Area)\
            .options(joinedload_all(Feature.chapter, Chapter.area))

    def col_defs(self):
        return [
            FeatureIdCol(self, 'id', sClass='right'),
            LinkCol(self, 'name'),
            ContributorsCol(self, 'Authors', bSearchable=False, bSortable=False),
            FeatureAreaCol(self, 'area'),
            Col(self, 'Languages', model_col=Feature.representation),
            DetailsRowLinkCol(self, 'd', button_text='Values'),
        ]


class CountriesCol(Col):
    __kw__ = dict(bSortable=False)

    def format(self, item):
        return HTML.ul(*[HTML.li(link(self.dt.req, c)) for c in item.countries], class_='unstyled')

    def search(self, qs):
        return icontains(Country.name, qs)


class Languages(datatables.Languages):
    def base_query(self, query):
        return query.outerjoin(WalsLanguage.countries).join(Genus).join(Family).options(
            joinedload_all(WalsLanguage.genus, Genus.family),
            joinedload(WalsLanguage.countries)).distinct()

    def col_defs(self):
        return [
            LinkCol(self, 'name'),
            IdCol(self, 'id', sTitle='WALS code', sClass='left'),
            Col(self, 'iso_codes', sTitle='ISO 639-3', model_col=WalsLanguage.iso_codes),
            LinkCol(self, 'genus', model_col=Genus.name, get_object=lambda i: i.genus),
            LinkCol(self, 'family', model_col=Family.name, get_object=lambda i: i.genus.family),
            Col(self, 'macroarea',
                model_col=WalsLanguage.macroarea,
                choices=get_distinct_values(WalsLanguage.macroarea)),
            Col(self, 'latitude'),
            Col(self, 'longitude'),
            CountriesCol(self, 'countries'),
        ]


class ChapterIdCol(Col):
    def format(self, item):
        return item.id if not item.id.startswith('s') else ''

    def order(self):
        return Chapter.sortkey


class ChapterAreaCol(_AreaCol):
    def format(self, item):
        return item.area.name if item.area else ''


class Chapters(datatables.Contributions):
    def base_query(self, query):
        return query.outerjoin(Area).options(joinedload(Chapter.area))

    def col_defs(self):
        cols = datatables.Contributions.col_defs(self)
        return [
            ChapterIdCol(self, 'id', bSearchable=False),
        ] + cols[:-1] + [
            ChapterAreaCol(self, 'area'),
        ] + cols[-1:]

    def get_options(self):
        return {'aaSorting': [[0, 'asc']]}


def includeme(config):
    config.register_datatable('contributions', Chapters)
    config.register_datatable('values', Datapoints)
    config.register_datatable('languages', Languages)
    config.register_datatable('parameters', Features)
