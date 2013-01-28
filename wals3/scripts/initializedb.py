from __future__ import unicode_literals
import os
import sys
import transaction
from collections import defaultdict

from sqlalchemy import engine_from_config, create_engine

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from clld.db.meta import (
    DBSession,
    VersionedDBSession,
    Base,
)
from clld.db.models import common

from wals3 import models


DB = 'sqlite:////home/robert/old_projects/legacy/wals_pylons/trunk/wals2/db.sqlite'


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)

    old_db = create_engine(DB)

    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    VersionedDBSession.configure(bind=engine)

    data = defaultdict(dict)

    def add(model, type, key, **kw):
        new = model(**kw)
        data[type][key] = new
        VersionedDBSession.add(new)
        return new

    with transaction.manager:
        for row in old_db.execute("select * from family"):
            add(models.Family, 'family', row['id'], id=row['id'], name=row['name'], description=row['comment'])

        for row in old_db.execute("select * from genus"):
            genus = add(models.Genus, 'genus', row['id'], name=row['name'])
            genus.family = data['family'][row['family_id']]

        for row in old_db.execute("select * from language"):
            kw = dict((key, row[key]) for key in ['id', 'name', 'latitude', 'longitude'])
            lang = add(models.WalsLanguage, 'language', row['id'],
                       samples_100=row['samples_100'] != 0, samples_200=row['samples_200'] != 0, **kw)
            lang.genus = data['genus'][row['genus_id']]

        for row in old_db.execute("select * from author"):
            add(common.Contributor, 'contributor', row['id'], name=row['name'], url=row['www'], id=row['id'], description=row['note'])
        VersionedDBSession.flush()

        for row in old_db.execute("select * from chapter"):
            add(models.Chapter, 'contribution', row['id'], id=row['id'], name=row['name'])
        VersionedDBSession.flush()

        for row in old_db.execute("select * from feature"):
            param = add(models.Feature, 'parameter', row['id'], id=row['id'], name=row['name'], ordinal_qualifier=row['id'][-1])
            param.chapter = data['contribution'][row['chapter_id']]
        VersionedDBSession.flush()

        for row in old_db.execute("select * from value"):
            desc = row['description']
            if desc == 'SOV & NegV/VNeg':
                if row['icon_id'] != 's9ff':
                    desc += ' (a)'
                else:
                    desc += ' (b)'

            domainelement = add(
                models.WalsValue, 'domainelement', (row['feature_id'], row['numeric']),
                id='%s-%s' % (row['feature_id'], row['numeric']),
                name=desc, description=row['long_description'], icon_id=row['icon_id'], numeric=row['numeric'])
            domainelement.parameter = data['parameter'][row['feature_id']]
        VersionedDBSession.flush()

        for row in old_db.execute("select * from datapoint"):
            value = add(common.Value, 'value', row['id'], id=row['id'])
            value.language = data['language'][row['language_id']]
            value.domainelement = data['domainelement'][(row['feature_id'], row['value_numeric'])]
            value.parameter = data['parameter'][row['feature_id']]
            value.contribution = data['parameter'][row['feature_id']].chapter

        VersionedDBSession.flush()

        for row in old_db.execute("select * from author_chapter"):

            new = common.ContributionContributor(
                ord=row['order'],
                primary=row['primary'] != 0,
                contributor_pk=data['contributor'][row['author_id']].pk,
                contribution_pk=data['contribution'][row['chapter_id']].pk)
            VersionedDBSession.add(new)

        lang.name = 'SPECIAL--' + lang.name


if __name__ == '__main__':
    main()
