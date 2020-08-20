"""python_seed.scripts.cli."""

import os
import shutil

import click

from .. import version


@click.group(short_help="python-seed CLI")
@click.version_option(version=version, message="%(version)s")
def pyseed():
    """python-seed subcommands."""
    pass


@pyseed.command(short_help="Create new python seed skeleton")
@click.argument("name", type=str, nargs=1)
def create(name):
    """Create new python seed skeleton."""
    template_dir = os.path.join(os.path.dirname(__file__), "../template")

    shutil.copytree(template_dir, name)

    new_dir = name
    name = name.replace("-", "_")
    for root, _, files in os.walk(new_dir):
        if root.endswith("pyseed"):
            shutil.move(root, root.replace("pyseed", name))

    for root, _, files in os.walk(new_dir):
        for filename in files:
            if filename.endswith(".pyc"):
                continue
            with open(f"{root}/{filename}", "r", encoding="utf-8") as f:
                s = f.read().replace("pyseed", name)

            with open(f"{root}/{filename}", "w", encoding="utf-8") as f:
                f.write(s)
