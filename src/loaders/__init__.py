"""
Loaders module.
Contains all data loading functionality for different file formats.
"""

from .data_loader import (
    FILE_TYPE_READERS,
    load_data_workflow,
    get_variable_names,
    get_file_list_by_type,
    load_data,
)
from .loading_utils import get_file_names, csv_reader, excel_reader, txt_reader
from .saving_utils import get_default_save_directory, save_dataframe

__all__ = [
    # Reader dispatch
    'FILE_TYPE_READERS',
    # Main workflow functions
    'load_data_workflow',
    'get_variable_names',
    'get_file_list_by_type',
    'load_data',
    # File utilities
    'get_file_names',
    'csv_reader',
    'excel_reader',
    'txt_reader',
    'get_default_save_directory',
    'save_dataframe',
]
