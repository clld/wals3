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
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property

from clld import interfaces
from clld.db.meta import Base, CustomModelMixin
from clld.db.versioned import Versioned
from clld.db.models.common import (
    Language,
    Parameter,
    DomainElement,
    Contribution,
    IdNameDescriptionMixin,
)
from wals3 import interfaces as wals_interfaces


@implementer(wals_interfaces.IFamily)
class Family(Base, IdNameDescriptionMixin):
    pass


@implementer(wals_interfaces.ICountry)
class Country(Base, IdNameDescriptionMixin):
    continent = Column(Unicode)

    @property
    def languages(self):
        return [assoc.language for assoc in self.language_assocs]


class CountryLanguage(Base):
    __table_args__ = (UniqueConstraint('country_pk', 'language_pk'),)

    country_pk = Column(Integer, ForeignKey('country.pk'))
    language_pk = Column(Integer, ForeignKey('language.pk'))

    country = relationship(Country, backref='language_assocs')
    language = relationship(Language, backref='country_assocs')


class Genus(Base, IdNameDescriptionMixin):
    family_pk = Column(Integer, ForeignKey('family.pk'))
    subfamily = Column(Unicode)
    family = relationship(Family, backref=backref("genera", order_by="Genus.subfamily, Genus.name"))
    icon_id = Column(String(4))


class Area(Base, IdNameDescriptionMixin):
    dbpedia_url = Column(String)


#-----------------------------------------------------------------------------
# specialized common mapper classes
#-----------------------------------------------------------------------------
@implementer(interfaces.ILanguage)
class WalsLanguage(Language, CustomModelMixin, Versioned):
    pk = Column(Integer, ForeignKey('language.pk'), primary_key=True)

    ascii_name = Column(String)
    genus_pk = Column(Integer, ForeignKey('genus.pk'))
    samples_100 = Column(Boolean, default=False)
    samples_200 = Column(Boolean, default=False)

    genus = relationship(Genus, backref=backref("languages", order_by="Language.name"))


@implementer(interfaces.IContribution)
class Chapter(Contribution, CustomModelMixin, Versioned):
    """Contributions in WALS are chapters chapters. These comprise a set of features with
    corresponding values and a descriptive text.
    """
    pk = Column(Integer, ForeignKey('contribution.pk'), primary_key=True)
    #id = Column(Integer, unique=True)
    blog_title = Column(Unicode)
    area_pk = Column(Integer, ForeignKey('area.pk'))
    area = relationship(Area, lazy='joined')


@implementer(interfaces.IParameter)
class Feature(Parameter, CustomModelMixin, Versioned):
    """Parameters in WALS are called feature. They are always related to one chapter.
    """
    __table_args__ = (UniqueConstraint('contribution_pk', 'ordinal_qualifier'),)

    pk = Column(Integer, ForeignKey('parameter.pk'), primary_key=True)
    contribution_pk = Column(Integer, ForeignKey('contribution.pk'))
    id = Column(String(5), unique=True)
    blog_title = Column(String(50), unique=True)
    chapter = relationship(Chapter, lazy='joined')
    ordinal_qualifier = Column(String)

    @property
    def sortkey(self):
        return self.contribution_pk, self.ordinal_qualifier


@implementer(interfaces.IDomainElement)
class WalsValue(DomainElement, CustomModelMixin):
    """All features in WALS have fixed lists of admissible values.
    """
    pk = Column(Integer, ForeignKey('domainelement.pk'), primary_key=True)
    icon_id = Column(String(4))
    numeric = Column(Integer)
