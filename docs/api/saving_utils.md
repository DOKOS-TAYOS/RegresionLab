# loaders.saving_utils

Save DataFrame to file (CSV, TXT, XLSX).

## Overview

The `saving_utils` module provides functions to save pandas DataFrames to disk. It complements `loading_utils` (which loads data) and is used by the View Data save dialog and Streamlit download functionality.

## Key Functions

#### `save_dataframe(data, file_path, file_type=None) -> str`

Save a DataFrame to file.

**Parameters:**
- `data`: DataFrame to save
- `file_path`: Full path to the output file
- `file_type`: Optional. 'csv', 'txt', or 'xlsx'. If None, inferred from path extension.

**Returns:**
- The path where the file was saved

**Raises:**
- `ValueError`: If file type is not supported

**Example:**
```python
from loaders.saving_utils import save_dataframe
import pandas as pd

df = pd.DataFrame({'x': [1, 2, 3], 'y': [2, 4, 6]})
save_dataframe(df, 'output/processed.csv')
# Or with explicit type:
save_dataframe(df, 'output/processed.xlsx', file_type='xlsx')
```

#### `get_default_save_directory() -> str`

Return the default directory for saving (typically the input folder from config).

**Returns:**
- Absolute path to the default save directory

**Example:**
```python
from loaders.saving_utils import get_default_save_directory

default_dir = get_default_save_directory()
# Use in file picker: initialdir=default_dir
```

## Supported Formats

- **CSV**: Comma-separated; NaN written as 'no' (consistent with loading).
- **TXT**: Tab-separated; NaN written as 'no'.
- **XLSX**: Excel format; requires openpyxl.
