import pytest


@pytest.yield_fixture
def in_tmpdir(tmpdir):
    """Change to pytest-provided temporary directory"""
    with tmpdir.as_cwd():
        yield tmpdir
