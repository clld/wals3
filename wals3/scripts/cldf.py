from sqlalchemy.orm import joinedload, contains_eager, joinedload_all

from clld.lib.dsv import UnicodeWriter
from clld.scripts.util import parsed_args, ExistingDir
from clld.db.meta import DBSession
from clld.db.models.common import Parameter, ValueSet, Language, ValueSetReference


def format_refs(req, obj):
    refs = []
    refs_names = []
    for r in obj.references:
        if r.source:
            refname = r.source.name
            ref = req.resource_url(r.source)
            if r.description:
                refname += '[%s]' % r.description
                ref += '[%s]' % r.description
            refs.append(ref)
            refs_names.append(refname)
    return ';'.join(refs), ';'.join(refs_names)


def write_cldf(req, feature, valuesets, fname):
    with UnicodeWriter(f=fname) as writer:
        writer.writerow(['LANGUAGE_NAME', 'VALUE', 'SOURCE_NAME', 'ID', 'LANGUAGE_ID', 'FEATURE_ID', 'SOURCE'])
        for vs in valuesets:
            source, source_name = format_refs(req, vs)
            writer.writerow([
                vs.language.name,
                vs.values[0].domainelement.name,
                source_name,
                req.resource_url(vs),
                req.resource_url(vs.language),
                req.resource_url(feature),
                source,
            ])


def main(args):
    features = list(DBSession.query(Parameter).options(joinedload(Parameter.domain)))

    for feature in features:
        valuesets = DBSession.query(ValueSet)\
            .join(Language)\
            .filter(ValueSet.parameter_pk == feature.pk)\
            .order_by(Language.name)\
            .options(
                contains_eager(ValueSet.language),
                joinedload(ValueSet.values),
                joinedload_all(ValueSet.references, ValueSetReference.source))
        write_cldf(
            args.env['request'],
            feature,
            valuesets,
            args.outdir.joinpath('feature-%s.cldf.csv' % feature.id))


if __name__ == '__main__':
    main(parsed_args((('outdir',), dict(action=ExistingDir)), bootstrap=True))
