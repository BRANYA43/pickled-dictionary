import click
from peewee_migrate import Router

import settings
from database import config

from .utils import danger, slugify, success, warning


# ==================================================================================================
# Callbacks
# ==================================================================================================
def slugify_callback(context, self, value):
    return slugify(value)


# ==================================================================================================
# Entry
# ==================================================================================================
@click.group()
@click.pass_context
def migrations(context: click.Context):
    """
    Migration Manager.
    """
    context.obj = Router(
        database=config.database,
        migrate_dir=settings.MIGRATION_DIR,
    )


# ==================================================================================================
# Create
# ==================================================================================================
@migrations.command()
@click.argument('name', callback=slugify_callback, metavar='MIGRATION_NAME')
@click.pass_obj
def create(router: Router, name: str):
    """
    Create a migration.
    """
    migration = router.create(name=name, auto=settings.MODEL_MODULE)
    if migration:
        click.echo(success(f'Migration "{migration}" was created.'))
    else:
        click.echo(warning('No changes detected to create a migration.'))


# ==================================================================================================
# Migrate
# ==================================================================================================
@migrations.command()
@click.argument('number', default='', metavar='MIGRATION_NUMBER')
@click.option('--first', is_flag=True, help='Migrate the first migration.')
@click.option('--fake', is_flag=True, help='Fake migration.')
@click.pass_obj
def migrate(router: Router, number: str, first: bool, fake: bool):
    """
    Apply migrations.

    If a MIGRATION_NUMBER is provided, apply all migrations up to and including that one.
    """
    if number and first:
        raise click.UsageError('Either set migration number or use "--first", not both.')

    undone = router.diff
    if not undone:
        click.echo(warning('No migrations detected to apply.'))
    elif number:
        index, migration = _search_migration(number, undone)
        if index is None:
            index, migration = _search_migration(number, router.done)
            if index is not None:
                click.echo(warning(f'Migration "{migration}" has already been applied.'))
            else:
                click.echo(warning(f'No migration found with number "{number}".'))
        else:
            _migrate(router, undone[: index + 1], fake=fake)
    elif first:
        _migrate(router, [undone[0]], fake=fake)
    else:
        _migrate(router, undone, fake=fake)


def _migrate(router: Router, migrations_: list[str], *, fake=False):

    click.echo('Migrating...')
    for m in migrations_:
        click.echo(f'  {m}', nl=False)
        router.run_one(name=m, migrator=router.migrator, fake=fake)
        click.echo(f' [{success("OK")}]')
    click.echo(f'Total migrations applied: {len(migrations_)}')


# ==================================================================================================
# Rollback
# ==================================================================================================
@migrations.command()
@click.argument('number', default='', metavar='MIGRATION_NUMBER')
@click.option('--last', is_flag=True, help='Roll back the latest migration.')
@click.option('--fake', is_flag=True, help='Fake the rollback.')
@click.pass_obj
def rollback(router: Router, number: str, last: bool, fake: bool):
    """
    Roll back applied migrations.

    If a MIGRATION_NUMBER is provided, roll back all migrations newer than and including that one.
    """
    if number and last:
        raise click.UsageError('Either set migration number or use "--last", not both.')

    done = router.done
    if not done:
        click.echo(warning('No migrations to roll back.'))
    elif number:
        index, migration = _search_migration(number, done)
        if index is None:
            index, migration = _search_migration(number, router.diff)
            if index is not None:
                click.echo(warning(f'Migration "{migration}" has not been applied.'))
            else:
                click.echo(warning(f'No migration found with number "{number}".'))
        else:
            _rollback(router, done[index:], fake=fake)
    elif last:
        _rollback(router, [done[-1]], fake=fake)
    else:
        _rollback(router, done, fake=fake)


def _rollback(router: Router, migrations_: list[str], *, fake=False):
    """
    Roll back migrations.
    """

    click.echo('Rolling back...')
    for m in migrations_[::-1]:
        click.echo(f'  {m}', nl=False)
        router.run_one(name=m, migrator=router.migrator, fake=fake, downgrade=True)
        click.echo(f' [{success("OK")}]')
    click.echo(f'Total migrations rolled back: {len(migrations_)}')


# ==================================================================================================
# Merge
# ==================================================================================================
@migrations.command()
@click.argument('name', callback=slugify_callback, metavar='MIGRATION_NAME')
@click.pass_obj
def merge(router: Router, name: str):
    """
    Merge all migrations into one.
    """
    if not router.todo:
        click.echo(warning('No migrations detected to merge.'))
    elif router.done:
        click.echo(warning('Must roll back all migrations before merging.'))
    else:
        click.echo('Merging...')
        router.merge(name)
        click.echo(success(f'Merged into migration "001_{name}".'))


# ==================================================================================================
# Clear
# ==================================================================================================
@migrations.command()
@click.pass_obj
def clear(router: Router):
    """
    Delete all migrations.
    """
    if not router.todo:
        click.echo(warning('No migrations detected to clear.'))
    elif router.done:
        click.echo(warning('Must roll back all migrations before clearing.'))
    else:
        click.echo('Clearing...')
        router.clear()
        click.echo(success('Migrations were deleted.'))


# ==================================================================================================
# List
# ==================================================================================================
@migrations.command('list')
@click.pass_obj
def list_(router: Router):
    """
    List migrations.
    """
    click.echo('Migrations:')
    if done := router.done:
        click.echo('\n'.join(f'[{success("X")}] {m}' for m in done))
    if undone := router.diff:
        click.echo('\n'.join(f'[{danger("-")}] {m}' for m in undone))


# ==================================================================================================
# Utils
# ==================================================================================================
def _search_migration(number: str, migrations_: list[str]) -> tuple[int, str] | tuple[None, None]:
    """
    Search for a migration by its number prefix.
    """
    return next(((i, m) for i, m in enumerate(migrations_) if m.startswith(number)), (None, None))
