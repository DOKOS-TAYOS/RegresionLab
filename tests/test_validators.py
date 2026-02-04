#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for validators module.
"""

import unittest
import sys
import tempfile
from pathlib import Path
import pandas as pd
import numpy as np

# Add src to path
src_path = Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(src_path))

from utils.validators import (
    validate_file_path,
    validate_file_type,
    validate_dataframe,
    validate_column_exists,
    validate_numeric_data,
    validate_uncertainty_column,
    validate_fitting_data,
    validate_parameter_names,
    validate_positive_integer
)
from utils.exceptions import (
    DataValidationError,
    FileNotFoundError,
    InvalidFileTypeError,
    ValidationError
)


class TestValidateFilePath(unittest.TestCase):
    """Tests for validate_file_path function."""
    
    def test_valid_file_path(self) -> None:
        """Test validation passes for valid file."""
        with tempfile.NamedTemporaryFile(delete=False) as tf:
            temp_path = tf.name
        try:
            validate_file_path(temp_path)
        finally:
            Path(temp_path).unlink(missing_ok=True)
    
    def test_nonexistent_file(self) -> None:
        """Test validation fails for nonexistent file."""
        with self.assertRaises(FileNotFoundError):
            validate_file_path('/nonexistent/path/file.txt')
    
    def test_directory_path(self) -> None:
        """Test validation fails for directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            with self.assertRaises(ValidationError):
                validate_file_path(temp_dir)


class TestValidateFileType(unittest.TestCase):
    """Tests for validate_file_type function."""
    
    def test_valid_csv(self) -> None:
        """Test validation passes for csv."""
        validate_file_type('csv')
    
    def test_valid_xlsx(self) -> None:
        """Test validation passes for xlsx."""
        validate_file_type('xlsx')
    
    def test_invalid_type(self) -> None:
        """Test validation fails for invalid type."""
        with self.assertRaises(InvalidFileTypeError):
            validate_file_type('pdf')
    
    def test_custom_allowed_types(self) -> None:
        """Test validation with custom allowed types."""
        validate_file_type('txt', allowed_types=['txt', 'dat'])
        with self.assertRaises(InvalidFileTypeError):
            validate_file_type('csv', allowed_types=['txt', 'dat'])


class TestValidateDataFrame(unittest.TestCase):
    """Tests for validate_dataframe function."""
    
    def test_valid_dataframe(self) -> None:
        """Test validation passes for valid DataFrame."""
        df = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
        validate_dataframe(df)
    
    def test_none_dataframe(self) -> None:
        """Test validation fails for None."""
        with self.assertRaises(DataValidationError):
            validate_dataframe(None)
    
    def test_empty_dataframe(self) -> None:
        """Test validation fails for empty DataFrame."""
        df = pd.DataFrame()
        with self.assertRaises(DataValidationError):
            validate_dataframe(df)
    
    def test_insufficient_rows(self) -> None:
        """Test validation fails for insufficient rows."""
        df = pd.DataFrame({'x': [1], 'y': [2]})
        with self.assertRaises(DataValidationError):
            validate_dataframe(df, min_rows=2)
    
    def test_custom_min_rows(self) -> None:
        """Test validation with custom min_rows."""
        df = pd.DataFrame({'x': [1, 2, 3, 4, 5]})
        validate_dataframe(df, min_rows=5)


class TestValidateColumnExists(unittest.TestCase):
    """Tests for validate_column_exists function."""
    
    def test_existing_column(self) -> None:
        """Test validation passes for existing column."""
        df = pd.DataFrame({'x': [1, 2], 'y': [3, 4]})
        validate_column_exists(df, 'x')
    
    def test_missing_column(self) -> None:
        """Test validation fails for missing column."""
        df = pd.DataFrame({'x': [1, 2]})
        with self.assertRaises(DataValidationError):
            validate_column_exists(df, 'y')


class TestValidateNumericData(unittest.TestCase):
    """Tests for validate_numeric_data function."""
    
    def test_valid_numeric(self) -> None:
        """Test validation passes for numeric data."""
        series = pd.Series([1.0, 2.0, 3.0])
        validate_numeric_data(series, 'test_col')
    
    def test_integer_data(self) -> None:
        """Test validation passes for integer data."""
        series = pd.Series([1, 2, 3])
        validate_numeric_data(series, 'test_col')
    
    def test_non_numeric(self) -> None:
        """Test validation fails for non-numeric data."""
        series = pd.Series(['a', 'b', 'c'])
        with self.assertRaises(DataValidationError):
            validate_numeric_data(series, 'test_col')
    
    def test_nan_values(self) -> None:
        """Test validation fails for NaN values."""
        series = pd.Series([1.0, np.nan, 3.0])
        with self.assertRaises(DataValidationError):
            validate_numeric_data(series, 'test_col')
    
    def test_infinite_values(self) -> None:
        """Test validation fails for infinite values."""
        series = pd.Series([1.0, np.inf, 3.0])
        with self.assertRaises(DataValidationError):
            validate_numeric_data(series, 'test_col')


class TestValidateUncertaintyColumn(unittest.TestCase):
    """Tests for validate_uncertainty_column function."""
    
    def test_valid_uncertainty(self) -> None:
        """Test validation passes for valid uncertainty column."""
        df = pd.DataFrame({'x': [1, 2, 3], 'ux': [0.1, 0.1, 0.1]})
        validate_uncertainty_column(df, 'x')
    
    def test_missing_uncertainty(self) -> None:
        """Test validation fails for missing uncertainty column."""
        df = pd.DataFrame({'x': [1, 2, 3]})
        with self.assertRaises(DataValidationError):
            validate_uncertainty_column(df, 'x')
    
    def test_negative_uncertainty(self) -> None:
        """Test validation fails for negative uncertainties."""
        df = pd.DataFrame({'x': [1, 2, 3], 'ux': [0.1, -0.1, 0.1]})
        with self.assertRaises(DataValidationError):
            validate_uncertainty_column(df, 'x')


class TestValidateFittingData(unittest.TestCase):
    """Tests for validate_fitting_data function."""
    
    def test_valid_fitting_data(self) -> None:
        """Test validation passes for valid fitting data."""
        df = pd.DataFrame({
            'x': [1.0, 2.0, 3.0],
            'ux': [0.1, 0.1, 0.1],
            'y': [2.0, 4.0, 6.0],
            'uy': [0.2, 0.2, 0.2]
        })
        validate_fitting_data(df, 'x', 'y')
    
    def test_missing_x_column(self) -> None:
        """Test validation fails for missing x column."""
        df = pd.DataFrame({
            'y': [2.0, 4.0, 6.0],
            'uy': [0.2, 0.2, 0.2]
        })
        with self.assertRaises(DataValidationError):
            validate_fitting_data(df, 'x', 'y')
    
    def test_missing_uncertainty(self) -> None:
        """Test validation fails for missing uncertainty columns."""
        df = pd.DataFrame({
            'x': [1.0, 2.0, 3.0],
            'y': [2.0, 4.0, 6.0]
        })
        with self.assertRaises(DataValidationError):
            validate_fitting_data(df, 'x', 'y')


class TestValidateParameterNames(unittest.TestCase):
    """Tests for validate_parameter_names function."""
    
    def test_valid_names(self) -> None:
        """Test validation passes for valid parameter names."""
        validate_parameter_names(['a', 'b', 'c'])
    
    def test_empty_list(self) -> None:
        """Test validation fails for empty list."""
        with self.assertRaises(ValidationError):
            validate_parameter_names([])
    
    def test_duplicate_names(self) -> None:
        """Test validation fails for duplicate names."""
        with self.assertRaises(ValidationError):
            validate_parameter_names(['a', 'b', 'a'])
    
    def test_invalid_identifier(self) -> None:
        """Test validation fails for invalid Python identifiers."""
        with self.assertRaises(ValidationError):
            validate_parameter_names(['123invalid'])
        with self.assertRaises(ValidationError):
            validate_parameter_names(['my-param'])


class TestValidatePositiveInteger(unittest.TestCase):
    """Tests for validate_positive_integer function."""
    
    def test_valid_positive_integer(self) -> None:
        """Test validation passes for positive integer."""
        result = validate_positive_integer(5, 'test_param')
        self.assertEqual(result, 5)
    
    def test_string_number(self) -> None:
        """Test validation passes for string number."""
        result = validate_positive_integer('10', 'test_param')
        self.assertEqual(result, 10)
    
    def test_zero(self) -> None:
        """Test validation fails for zero."""
        with self.assertRaises(ValidationError):
            validate_positive_integer(0, 'test_param')
    
    def test_negative(self) -> None:
        """Test validation fails for negative."""
        with self.assertRaises(ValidationError):
            validate_positive_integer(-5, 'test_param')
    
    def test_non_integer(self) -> None:
        """Test validation fails for non-integer."""
        with self.assertRaises(ValidationError):
            validate_positive_integer('not_a_number', 'test_param')


if __name__ == '__main__':
    unittest.main()
