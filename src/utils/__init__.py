#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Utils module.
Contains utility functions including exceptions, logging, and validation.
"""

from .exceptions import (
    RegressionLabError,
    DataLoadError,
    DataValidationError,
    FileNotFoundError,
    InvalidFileTypeError,
    FittingError,
    EquationError,
    ConfigurationError,
    ValidationError,
)
from .logger import (
    setup_logging,
    get_logger,
    ColoredFormatter,
)
from .validators import (
    validate_dataframe,
    validate_data_format,
    validate_file_path,
    validate_file_type,
    validate_parameter_names,
    parse_optional_float,
    validate_fitting_data,
)

__all__ = [
    # Exceptions
    'RegressionLabError',
    'DataLoadError',
    'DataValidationError',
    'FileNotFoundError',
    'InvalidFileTypeError',
    'FittingError',
    'EquationError',
    'ConfigurationError',
    'ValidationError',
    # Logger
    'setup_logging',
    'get_logger',
    'ColoredFormatter',
    # Validators
    'validate_dataframe',
    'validate_data_format',
    'validate_file_path',
    'validate_file_type',
    'validate_parameter_names',
    'parse_optional_float',
    'validate_fitting_data',
]
