"""pyseed.scripts.cli: pyseed CLI."""

import click

from .. import __version__


@click.group(short_help="pyseed CLI")
@click.version_option(version=__version__, message="%(version)s")
def pyseed():
    """pyseed subcommands."""
    print(f"pyseed {__version__} is installed.")


# @pyseed.command(short_help="Validate COGEO")
# @click.option(...)
# def cmd(...):
#     """Do Great Things."""
#     pass
