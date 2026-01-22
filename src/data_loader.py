"""
Data loading utilities for the project.
"""

import pandas as pd
import logging
from pathlib import Path
from typing import Tuple

logger = logging.getLogger(__name__)


def load_data(filepath: str) -> pd.DataFrame:
    """
    Load data from a CSV or Excel file.

    Args:
        filepath: Path to the data file

    Returns:
        Loaded DataFrame

    Raises:
        FileNotFoundError: If the file doesn't exist
        ValueError: If the file format is not supported
    """
    filepath = Path(filepath)

    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    if filepath.suffix == ".csv":
        data = pd.read_csv(filepath)
    elif filepath.suffix in [".xlsx", ".xls"]:
        data = pd.read_excel(filepath)
    else:
        raise ValueError(f"Unsupported file format: {filepath.suffix}")

    logger.info(f"Loaded data from {filepath}. Shape: {data.shape}")
    return data


def save_data(data: pd.DataFrame, filepath: str) -> None:
    """
    Save DataFrame to a file.

    Args:
        data: DataFrame to save
        filepath: Output file path
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    if filepath.suffix == ".csv":
        data.to_csv(filepath, index=False)
    elif filepath.suffix in [".xlsx", ".xls"]:
        data.to_excel(filepath, index=False)
    else:
        raise ValueError(f"Unsupported file format: {filepath.suffix}")

    logger.info(f"Saved data to {filepath}")


def split_data(
    data: pd.DataFrame, test_size: float = 0.2, random_state: int = 42
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Split data into training and testing sets.

    Args:
        data: Input DataFrame
        test_size: Proportion of test set
        random_state: Random state for reproducibility

    Returns:
        Tuple of (train_data, test_data)
    """
    from sklearn.model_selection import train_test_split

    train_data, test_data = train_test_split(
        data, test_size=test_size, random_state=random_state
    )
    logger.info(f"Split data: {len(train_data)} train, {len(test_data)} test")
    return train_data, test_data
