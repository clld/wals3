from sqlalchemy import and_, desc
from sqlalchemy.orm import joinedload
from sqlalchemy.sql.expression import cast
from sqlalchemy.types import Integer

from clld.web import datatables
from clld.web.datatables.base import Col, filter_number, LinkCol
from clld.db.models import common
from clld.web.util.helpers import linked_contributors
from clld.web.util.htmllib import HTML
from clld.db.meta import DBSession

from wals3.models import WalsLanguage, Genus, Family, Chapter, Feature


class ContributorsCol(Col):
    def format(self, item):
        return linked_contributors(self.dt.req, item.chapter)


class RepresentationCol(Col):
    def search(self, qs):
        return filter_number(cast(common.Parameter_data.value, Integer), qs, type_=int)

    def order(self):
        return cast(common.Parameter_data.value, Integer)

    def format(self, item):
        return item.datadict()['representation']


class IdCol(Col):
    def order(self):
        return Feature.contribution_pk, Feature.ordinal_qualifier


class Features(datatables.Parameters):
    def base_query(self, query):
        return query.join(Chapter)\
            .join(common.Parameter_data, and_(
                common.Parameter_data.object_pk == common.Parameter.pk,
                common.Parameter_data.key == 'representation'
            ))\
            .options(joinedload(Feature.chapter), joinedload(common.Parameter.data))

    def col_defs(self):
        return [
            IdCol(self, 'id', sClass='right'),
            LinkCol(self, 'name'),
            ContributorsCol(self, 'Authors', bSearchable=False, bSortable=False),
            RepresentationCol(self, 'Languages', sClass='right'),
        ]


class GenusCol(Col):
    def order(self):
        return Genus.name

    def search(self, qs):
        return Genus.name.contains(qs)

    def format(self, item):
        return item.genus.name


class Languages(datatables.Languages):
    def base_query(self, query):
        return query.join(Genus).join(Family).options(joinedload(WalsLanguage.genus))

    def col_defs(self):
        cols = datatables.Languages.col_defs(self)
        return cols[:2] + [GenusCol(self, 'genus')] + cols[2:]
