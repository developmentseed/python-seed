"""tests python_seed.cli."""

import os

from click.testing import CliRunner

from python_seed.scripts.cli import pyseed


def test_create():
    """Test the create function"""
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(pyseed, ["create", "myfunction"])
        assert not os.path.exists("myfunction/.github/workflows/ci.yml")
        assert not os.path.exists("myfunction/codecov.yml")
        with open("myfunction/README.md", "r") as f:
            assert f.read().splitlines()[0] == "# myfunction"
        assert not result.exception
        assert result.exit_code == 0

    with runner.isolated_filesystem():
        result = runner.invoke(pyseed, ["create", "myfunction", "--ci", "github"])
        assert os.path.exists("myfunction/.github/workflows/ci.yml")
        assert os.path.exists("myfunction/codecov.yml")
        with open("myfunction/README.md", "r") as f:
            assert f.read().splitlines()[0] == "# myfunction"
        assert not result.exception
        assert result.exit_code == 0
