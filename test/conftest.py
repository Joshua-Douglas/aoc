import sys
from pathlib import Path

import pytest

# Quick & Dirty since I don't really need a package for my aoc solutions
sys.path.append(str(Path(__file__).resolve().parent.parent))

@pytest.fixture
def data_dir() -> Path:
    """
    Fixture to return the absolute path to the /data directory inside the test directory.
    """
    return Path(__file__).resolve().parent / "data"