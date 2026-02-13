"""Save DataFrame to file (CSV, TXT, XLSX)."""

from pathlib import Path
from typing import Optional

import pandas as pd

from config import FILE_CONFIG, get_project_root
from utils import get_logger

logger = get_logger(__name__)


def save_dataframe(
    data: pd.DataFrame,
    file_path: str,
    file_type: Optional[str] = None,
) -> str:
    """
    Save a DataFrame to file.

    Args:
        data: DataFrame to save.
        file_path: Full path to the output file.
        file_type: 'csv', 'txt', or 'xlsx'. If None, inferred from path extension.

    Returns:
        The path where the file was saved.

    Raises:
        ValueError: If file type is not supported.
    """
    path = Path(file_path)
    if file_type is None:
        ext = path.suffix.lower().lstrip('.')
        file_type = ext if ext in ('csv', 'txt', 'xlsx') else 'csv'

    path.parent.mkdir(parents=True, exist_ok=True)

    if file_type == 'csv':
        data.to_csv(path, index=False, na_rep='no')
    elif file_type == 'txt':
        data.to_csv(path, sep='\t', index=False, na_rep='no')
    elif file_type == 'xlsx':
        data.to_excel(path, index=False)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")

    logger.info(f"Data saved to {path}")
    return str(path)


def get_default_save_directory() -> str:
    """Return the default directory for saving (input folder)."""
    root = get_project_root()
    return str(root / FILE_CONFIG['input_dir'])
