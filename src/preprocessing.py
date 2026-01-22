"""
Data preprocessing utilities.
"""

import pandas as pd
import numpy as np
import logging
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder

logger = logging.getLogger(__name__)


def handle_missing_values(data: pd.DataFrame, strategy: str = "mean") -> pd.DataFrame:
    """
    Handle missing values in the dataset.

    Args:
        data: Input DataFrame
        strategy: Strategy for handling missing values ('mean', 'median', 'drop')

    Returns:
        DataFrame with missing values handled
    """
    data = data.copy()

    if strategy == "drop":
        data = data.dropna()
    elif strategy == "mean":
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        data[numeric_cols] = data[numeric_cols].fillna(data[numeric_cols].mean())
    elif strategy == "median":
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        data[numeric_cols] = data[numeric_cols].fillna(data[numeric_cols].median())

    logger.info(f"Handled missing values using strategy: {strategy}")
    return data


def scale_features(
    data: pd.DataFrame, method: str = "standard", columns: list = None
) -> Tuple[pd.DataFrame, object]:
    """
    Scale numerical features.

    Args:
        data: Input DataFrame
        method: Scaling method ('standard', 'minmax')
        columns: Columns to scale (if None, scales all numeric columns)

    Returns:
        Scaled DataFrame and scaler object
    """
    data = data.copy()

    if columns is None:
        columns = data.select_dtypes(include=[np.number]).columns

    if method == "standard":
        scaler = StandardScaler()
    elif method == "minmax":
        scaler = MinMaxScaler()
    else:
        raise ValueError(f"Unknown scaling method: {method}")

    data[columns] = scaler.fit_transform(data[columns])
    logger.info(f"Scaled {len(columns)} features using {method} scaling")

    return data, scaler


def encode_categorical(data: pd.DataFrame, columns: list = None) -> Tuple[pd.DataFrame, dict]:
    """
    Encode categorical features.

    Args:
        data: Input DataFrame
        columns: Columns to encode (if None, encodes all object columns)

    Returns:
        DataFrame with encoded features and encoder mapping
    """
    from sklearn.preprocessing import LabelEncoder

    data = data.copy()

    if columns is None:
        columns = data.select_dtypes(include=["object"]).columns

    encoders = {}
    for col in columns:
        le = LabelEncoder()
        data[col] = le.fit_transform(data[col].astype(str))
        encoders[col] = le

    logger.info(f"Encoded {len(columns)} categorical features")
    return data, encoders
