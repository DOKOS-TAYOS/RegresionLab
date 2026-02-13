"""Data cleaning operations."""

from typing import List, Optional

import numpy as np
import pandas as pd

from utils import get_logger

logger = get_logger(__name__)

# Cleaning identifiers for UI
CLEAN_DROP_NA = 'drop_na'
CLEAN_DROP_DUPLICATES = 'drop_duplicates'
CLEAN_FILL_NA_MEAN = 'fill_na_mean'
CLEAN_FILL_NA_MEDIAN = 'fill_na_median'
CLEAN_FILL_NA_ZERO = 'fill_na_zero'
CLEAN_REMOVE_OUTLIERS_IQR = 'remove_outliers_iqr'
CLEAN_REMOVE_OUTLIERS_ZSCORE = 'remove_outliers_zscore'

CLEAN_OPTIONS: dict[str, str] = {
    CLEAN_DROP_NA: 'Drop rows with NaN',
    CLEAN_DROP_DUPLICATES: 'Drop duplicate rows',
    CLEAN_FILL_NA_MEAN: 'Fill NaN with column mean',
    CLEAN_FILL_NA_MEDIAN: 'Fill NaN with column median',
    CLEAN_FILL_NA_ZERO: 'Fill NaN with 0',
    CLEAN_REMOVE_OUTLIERS_IQR: 'Remove outliers (IQR method)',
    CLEAN_REMOVE_OUTLIERS_ZSCORE: 'Remove outliers (z-score)',
}


def _get_numeric_columns(data: pd.DataFrame, columns: Optional[List[str]] = None) -> List[str]:
    """Return numeric column names from data."""
    if columns is None:
        return list(data.select_dtypes(include=['number']).columns)
    return [c for c in columns if c in data.columns and pd.api.types.is_numeric_dtype(data[c])]


def apply_cleaning(
    data: pd.DataFrame,
    clean_id: str,
    columns: Optional[List[str]] = None,
) -> pd.DataFrame:
    """
    Apply a cleaning operation to the DataFrame.

    Args:
        data: Input DataFrame.
        clean_id: One of CLEAN_* constants.
        columns: For column-specific ops (fill, outliers). If None, all numeric.

    Returns:
        New cleaned DataFrame.
    """
    result = data.copy()

    if clean_id == CLEAN_DROP_NA:
        before = len(result)
        result = result.dropna()
        logger.info(f"Dropped {before - len(result)} rows with NaN")
        return result

    if clean_id == CLEAN_DROP_DUPLICATES:
        before = len(result)
        result = result.drop_duplicates()
        logger.info(f"Dropped {before - len(result)} duplicate rows")
        return result

    cols = _get_numeric_columns(result, columns) if columns else _get_numeric_columns(result)

    if clean_id == CLEAN_FILL_NA_MEAN:
        for col in cols:
            result[col] = result[col].fillna(result[col].mean())
        return result

    if clean_id == CLEAN_FILL_NA_MEDIAN:
        for col in cols:
            result[col] = result[col].fillna(result[col].median())
        return result

    if clean_id == CLEAN_FILL_NA_ZERO:
        for col in cols:
            result[col] = result[col].fillna(0)
        return result

    if clean_id == CLEAN_REMOVE_OUTLIERS_IQR:
        if not cols:
            return result
        mask = pd.Series(True, index=result.index)
        for col in cols:
            q1 = result[col].quantile(0.25)
            q3 = result[col].quantile(0.75)
            iqr = q3 - q1
            if iqr == 0:
                continue
            lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
            mask &= (result[col] >= lo) & (result[col] <= hi)
        before = len(result)
        result = result[mask]
        logger.info(f"IQR outliers: dropped {before - len(result)} rows")
        return result

    if clean_id == CLEAN_REMOVE_OUTLIERS_ZSCORE:
        if not cols:
            return result
        mask = pd.Series(True, index=result.index)
        for col in cols:
            mean = result[col].mean()
            std = result[col].std()
            if std == 0:
                continue
            z = np.abs((result[col] - mean) / std)
            mask &= (z <= 3)
        before = len(result)
        result = result[mask]
        logger.info(f"Z-score outliers: dropped {before - len(result)} rows")
        return result

    raise ValueError(f"Unknown cleaning: {clean_id}")
