"""pyseed.scripts.cli: pyseed CLI."""

import click

from .. import version


@click.group(short_help="pyseed CLI")
@click.version_option(version=version, message="%(version)s")
def pyseed():
    """pyseed subcommands."""
    pass


# @pyseed.command(short_help="Validate COGEO")
# @click.option(...)
# def cmd(...):
#     """Do Great Things."""
#     pass
