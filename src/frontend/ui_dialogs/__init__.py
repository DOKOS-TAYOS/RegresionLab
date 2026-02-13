"""
UI Dialogs package.
Contains all Tkinter dialog windows for user interaction, split by concern.
"""

from .data_selection import (
    ask_variables,
    ask_multiple_x_variables,
    show_data_dialog,
)
from .load_data_dialog import open_load_dialog
from .equation import (
    ask_equation_type,
    ask_num_parameters,
    ask_parameter_names,
    ask_custom_formula,
    ask_num_fits,
)
from .help import show_data_view_help_dialog, show_help_dialog, remove_markdown_bold
from .config_dialog import show_config_dialog
from .result import create_result_window
from .save_data_dialog import open_save_dialog

__all__ = [
    'ask_variables',
    'ask_multiple_x_variables',
    'show_data_dialog',
    'open_load_dialog',
    'ask_equation_type',
    'ask_num_parameters',
    'ask_parameter_names',
    'ask_custom_formula',
    'ask_num_fits',
    'show_data_view_help_dialog',
    'show_help_dialog',
    'remove_markdown_bold',
    'show_config_dialog',
    'create_result_window',
    'open_save_dialog',
]
