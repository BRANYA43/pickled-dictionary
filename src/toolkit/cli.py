import click

from .migrations import migrations


@click.group()
def cli():
    """Toolkit"""


cli.add_command(migrations)
