"""Test pyseed functions."""

from pyseed import app


def test_app():
    """Test app.dup_strings function."""
    assert app.dup_strings("ah ", 3) == "ah ah ah "
