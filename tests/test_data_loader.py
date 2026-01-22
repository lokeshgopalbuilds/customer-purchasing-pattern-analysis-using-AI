"""
Tests for data loader module.
"""

import pytest
import pandas as pd
import tempfile
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data_loader import load_data, save_data


@pytest.fixture
def sample_dataframe():
    """Create a sample dataframe for testing."""
    return pd.DataFrame({
        "customer_id": [1, 2, 3, 4, 5],
        "purchase_amount": [100.0, 150.0, 200.0, 75.0, 300.0],
        "category": ["Electronics", "Clothing", "Electronics", "Books", "Clothing"]
    })


def test_save_and_load_csv(sample_dataframe):
    """Test saving and loading CSV files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = Path(tmpdir) / "test_data.csv"
        save_data(sample_dataframe, str(filepath))
        loaded_data = load_data(str(filepath))
        pd.testing.assert_frame_equal(sample_dataframe, loaded_data)


def test_load_nonexistent_file():
    """Test loading a non-existent file."""
    with pytest.raises(FileNotFoundError):
        load_data("/nonexistent/path/file.csv")


def test_unsupported_format():
    """Test loading unsupported file format."""
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = Path(tmpdir) / "test_data.txt"
        filepath.write_text("test")
        with pytest.raises(ValueError):
            load_data(str(filepath))
