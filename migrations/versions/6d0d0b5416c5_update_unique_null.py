# coding=utf-8
"""update unique null

Revision ID: 6d0d0b5416c5
Revises: 671bd03f6cd
Create Date: 2018-01-10 08:38:55.689015

"""
from __future__ import unicode_literals

# revision identifiers, used by Alembic.
revision = '6d0d0b5416c5'
down_revision = u'671bd03f6cd'

import datetime

from alembic import op
import sqlalchemy as sa


UNIQUE_NULL = [
    ('contributioncontributor',
        ['contribution_pk', 'contributor_pk'], []),
    ('contributionreference',
        ['contribution_pk', 'source_pk', 'description'],
        ['description']),
    ('domainelement',
        ['parameter_pk', 'name'],
        ['name']),
    ('domainelement',
        ['parameter_pk', 'number'],
        ['number']),
    ('editor',
        ['dataset_pk', 'contributor_pk'], []),
    ('languageidentifier',
        ['language_pk', 'identifier_pk'], []),
    ('languagesource',
        ['language_pk', 'source_pk'], []),
    ('sentencereference',
        ['sentence_pk', 'source_pk', 'description'],
        ['description']),
    ('unit',
        ['language_pk', 'id'],
        ['id']),
    ('unitdomainelement',
        ['unitparameter_pk', 'name'],
        ['name']),
    ('unitdomainelement',
        ['unitparameter_pk', 'ord'],
        ['ord']),
    # NOTE: <unit, unitparameter, contribution> can have multiple values and also
    # multiple unitdomainelements
    ('unitvalue',
        [
            'unit_pk',
            'unitparameter_pk',
            'contribution_pk',
            'name',
            'unitdomainelement_pk'],
        ['contribution_pk', 'name', 'unitdomainelement_pk']),
    # NOTE: <language, parameter, contribution> can have multiple values and also
    # multiple domainelements
    ('value',
        ['valueset_pk', 'name', 'domainelement_pk'],
        ['name', 'domainelement_pk']),
    ('valuesentence',
        ['value_pk', 'sentence_pk'], []),
    ('valueset',
        ['language_pk', 'parameter_pk', 'contribution_pk'],
        ['contribution_pk']),
    ('valuesetreference',
        ['valueset_pk', 'source_pk', 'description'],
        ['description']),
]


class DryRunException(Exception):
    """Raised at the end of a dry run so the database transaction is not comitted."""


def upgrade(dry=False, verbose=True):
    conn = op.get_bind()

    assert conn.dialect.name == 'postgresql'

    def delete_null_duplicates(tablename, columns, notnull, returning=sa.text('*')):
        assert columns
        table = sa.table(tablename, *map(sa.column, ['pk'] + columns))
        any_null = sa.or_(table.c[n] == sa.null() for n in notnull)
        yield table.delete(bind=conn).where(any_null).returning(returning)
        other = table.alias()
        yield table.delete(bind=conn).where(~any_null).returning(returning)\
            .where(
                sa.exists()
                .where(sa.and_(table.c[c] == other.c[c] for c in columns))
                .where(table.c.pk > other.c.pk))

    def print_rows(rows, verbose=verbose):
        if not verbose:
            return
        for r in rows:
            print('    %r' % dict(r))

    class regclass(sa.types.UserDefinedType):
        def get_col_spec(self):
            return 'regclass'

    pga = sa.table(
        'pg_attribute', *map(sa.column, ['attrelid', 'attname', 'attnum', 'attnotnull']))

    select_nullable = sa.select([pga.c.attname], bind=conn)\
        .where(pga.c.attrelid == sa.cast(sa.bindparam('table'), regclass))\
        .where(pga.c.attname == sa.func.any(sa.bindparam('notnull')))\
        .where(~pga.c.attnotnull)\
        .order_by(pga.c.attnum)

    pgco = sa.table('pg_constraint', *map(sa.column,
                    ['oid', 'conname', 'contype', 'conrelid', 'conkey']))

    sq = sa.select([
        pgco.c.conname.label('name'),
        sa.func.pg_get_constraintdef(pgco.c.oid).label('definition'),
        sa.func.array(
            sa.select([sa.cast(pga.c.attname, sa.Text)])
            .where(pga.c.attrelid == pgco.c.conrelid)
            .where(pga.c.attnum == sa.func.any(pgco.c.conkey))
            .as_scalar()).label('names'),
    ])\
        .where(pgco.c.contype == 'u')\
        .where(pgco.c.conrelid == sa.cast(sa.bindparam('table'), regclass))\
        .alias()

    select_const = sa.select([sq.c.name, sq.c.definition], bind=conn)\
        .where(sq.c.names.op('@>')(sa.bindparam('cols')))\
        .where(sq.c.names.op('<@')(sa.bindparam('cols')))

    for table, unique, null in UNIQUE_NULL:
        print(table)
        notnull = [u for u in unique if u not in null]
        delete_null, delete_duplicates = delete_null_duplicates(table, unique, notnull)

        nulls = delete_null.execute().fetchall()
        if nulls:
            print('%s delete %d row(s) violating NOT NULL(%s)' % (
                table, len(nulls), ', '.join(notnull)))
            print_rows(nulls)

        duplicates = delete_duplicates.execute().fetchall()
        if duplicates:
            print('%s delete %d row(s) violating UNIQUE(%s)' % (
                table, len(duplicates), ', '.join(unique)))
            print_rows(duplicates)

        for col, in select_nullable.execute(table=table, notnull=notnull):
            print('%s alter column %s NOT NULL' % (table, col))
            op.alter_column(table, col, nullable=False)

        constraint = 'UNIQUE (%s)' % ', '.join(unique)
        matching = select_const.execute(table=table, cols=unique).fetchall()
        if matching:
            assert len(matching) == 1
            (name, definition), = matching
            if definition == constraint:
                print('%s keep constraint %s %s\n' % (table, name, definition))
                continue
            print('%s drop constraint %s %s' % (table, name, definition))
            op.drop_constraint(name, table)
        name = '%s_%s_key' % (table, '_'.join(unique))
        print('%s create constraint %s %s' % (table, name, constraint))
        op.create_unique_constraint(name, table, unique)
        print('')

    if dry:
        raise DryRunException('set dry=False to apply these changes')


def downgrade():
    pass
