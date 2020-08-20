"""tests python_seed.cli."""


from click.testing import CliRunner

from python_seed.scripts.cli import pyseed


def test_create():
    """Test the create function"""
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(pyseed, ["create", "myfunction"])
        with open("myfunction/README.md", "r") as f:
            assert f.read().splitlines()[0] == "# myfunction"
        assert not result.exception
        assert result.exit_code == 0
