import pytest


@pytest.fixture
def in_tmpdir(tmpdir):
    """Change to pytest-provided temporary directory"""
    tmpdir.chdir()
