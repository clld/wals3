import transaction

from clld.scripts.util import parsed_args
from clld.db.meta import VersionedDBSession
from clld.db.models import common


VALUES = {
    'cha': 'Words derived from Sinitic cha',
    'te': 'Words derived from Min Nan Chinese te',
}


def main(args):
    with transaction.manager:
        param = VersionedDBSession.query(common.Parameter) \
            .filter(common.Parameter.id == '138A') \
            .one()
        for de in param.domain:
            for k, v in VALUES.items():
                if v == de.name:
                    VALUES[k] = de

        for lid, value in [('lat', 'te'), ('dhi', 'cha'), ('chp', 'te')]:
            vs = VersionedDBSession.query(common.ValueSet)\
                .join(common.Language)\
                .filter(common.Language.id == lid)\
                .filter(common.ValueSet.parameter_pk == param.pk)\
                .one()
            de = VALUES[value]
            assert vs.values[0].domainelement != de
            vs.values[0].domainelement = de


if __name__ == "__main__":
    main(parsed_args())
