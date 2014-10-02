from zope.interface import implementer
from sqlalchemy import (
    Column,
    String,
    Unicode,
    Integer,
    Boolean,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship, backref

from clld import interfaces
from clld.db.meta import Base, CustomModelMixin
from clld.db.versioned import Versioned
from clld.db.models.common import (
    Language,
    Parameter,
    Contribution,
    IdNameDescriptionMixin,
    ValueSet,
)
from wals3 import interfaces as wals_interfaces


ValueSet.wp_slug = property(lambda self: 'datapoint-%s-wals_code_%s' % (
    self.parameter.id.lower(), self.language.id))


@implementer(wals_interfaces.IFamily)
class Family(Base, IdNameDescriptionMixin):
    pass


class CountryLanguage(Base):
    __table_args__ = (UniqueConstraint('country_pk', 'language_pk'),)

    country_pk = Column(Integer, ForeignKey('country.pk'))
    language_pk = Column(Integer, ForeignKey('language.pk'))


@implementer(wals_interfaces.ICountry)
class Country(Base, IdNameDescriptionMixin):
    continent = Column(Unicode)
    languages = relationship(
        Language, secondary=CountryLanguage.__table__, backref='countries')


@implementer(wals_interfaces.IGenus)
class Genus(Base, IdNameDescriptionMixin):
    family_pk = Column(Integer, ForeignKey('family.pk'))
    subfamily = Column(Unicode)
    family = relationship(
        Family, backref=backref("genera", order_by="Genus.subfamily, Genus.name"))
    icon = Column(String(7))


class Area(Base, IdNameDescriptionMixin):
    dbpedia_url = Column(String)


# ----------------------------------------------------------------------------
# specialized common mapper classes
# ----------------------------------------------------------------------------
@implementer(interfaces.ILanguage)
class WalsLanguage(Language, CustomModelMixin, Versioned):
    pk = Column(Integer, ForeignKey('language.pk'), primary_key=True)

    ascii_name = Column(String)
    genus_pk = Column(Integer, ForeignKey('genus.pk'))
    samples_100 = Column(Boolean, default=False)
    samples_200 = Column(Boolean, default=False)

    macroarea = Column(Unicode)
    iso_codes = Column(String)
    genus = relationship(Genus, backref=backref("languages", order_by="Language.name"))

    def __rdf__(self, request):
        yield 'skos:broader', request.resource_url(self.genus)
        if self.macroarea:
            yield 'dcterms:spatial', self.macroarea
        for country in self.countries:
            yield 'dcterms:spatial', 'http://www.geonames.org/countries/%s/' % country.id


@implementer(interfaces.IContribution)
class Chapter(Contribution, CustomModelMixin, Versioned):
    """Contributions in WALS are chapters chapters. These comprise a set of features with
    corresponding values and a descriptive text.
    """
    pk = Column(Integer, ForeignKey('contribution.pk'), primary_key=True)
    sortkey = Column(Integer)
    wp_slug = Column(Unicode)
    area_pk = Column(Integer, ForeignKey('area.pk'))
    area = relationship(Area, lazy='joined')

    def __rdf__(self, request):
        if self.area and self.area.dbpedia_url:
            yield 'dcterms:subject', self.area.dbpedia_url


@implementer(interfaces.IParameter)
class Feature(Parameter, CustomModelMixin, Versioned):
    """Parameters in WALS are called feature. They are always related to one chapter.
    """
    __table_args__ = (UniqueConstraint('contribution_pk', 'ordinal_qualifier'),)

    pk = Column(Integer, ForeignKey('parameter.pk'), primary_key=True)
    contribution_pk = Column(Integer, ForeignKey('contribution.pk'))
    blog_title = Column(String(50), unique=True)
    representation = Column(Integer)
    chapter = relationship(Chapter, lazy='joined', backref="features")
    ordinal_qualifier = Column(String)

    def __solr__(self, req):
        res = Parameter.__solr__(self, req)
        res.update(area_t=self.chapter.area.name)
        return res

    def __rdf__(self, request):
        if self.chapter.area.dbpedia_url:
            yield 'dcterms:subject', self.chapter.area.dbpedia_url
