#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for custom exceptions.
"""

import unittest
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(src_path))

from utils.exceptions import (
    RegressionLabError,
    DataLoadError,
    DataValidationError,
    FileNotFoundError,
    InvalidFileTypeError,
    FittingError,
    EquationError,
    ConfigurationError,
    ValidationError
)


class TestExceptionHierarchy(unittest.TestCase):
    """Tests for exception class hierarchy."""
    
    def test_regressionlab_error_base(self) -> None:
        """Test RegressionLabError is base exception."""
        self.assertTrue(issubclass(RegressionLabError, Exception))
    
    def test_data_load_error(self) -> None:
        """Test DataLoadError inherits from RegressionLabError."""
        self.assertTrue(issubclass(DataLoadError, RegressionLabError))
    
    def test_data_validation_error(self) -> None:
        """Test DataValidationError inherits from RegressionLabError."""
        self.assertTrue(issubclass(DataValidationError, RegressionLabError))
    
    def test_file_not_found_error(self) -> None:
        """Test FileNotFoundError inherits from DataLoadError."""
        self.assertTrue(issubclass(FileNotFoundError, DataLoadError))
    
    def test_invalid_file_type_error(self) -> None:
        """Test InvalidFileTypeError inherits from DataLoadError."""
        self.assertTrue(issubclass(InvalidFileTypeError, DataLoadError))
    
    def test_fitting_error(self) -> None:
        """Test FittingError inherits from RegressionLabError."""
        self.assertTrue(issubclass(FittingError, RegressionLabError))
    
    def test_equation_error(self) -> None:
        """Test EquationError inherits from RegressionLabError."""
        self.assertTrue(issubclass(EquationError, RegressionLabError))
    
    def test_configuration_error(self) -> None:
        """Test ConfigurationError inherits from RegressionLabError."""
        self.assertTrue(issubclass(ConfigurationError, RegressionLabError))
    
    def test_validation_error(self) -> None:
        """Test ValidationError inherits from RegressionLabError."""
        self.assertTrue(issubclass(ValidationError, RegressionLabError))


class TestExceptionRaising(unittest.TestCase):
    """Tests for raising and catching exceptions."""
    
    def test_raise_regressionlab_error(self) -> None:
        """Test raising RegressionLabError."""
        with self.assertRaises(RegressionLabError):
            raise RegressionLabError("Test error")
    
    def test_raise_data_load_error(self) -> None:
        """Test raising DataLoadError."""
        with self.assertRaises(DataLoadError):
            raise DataLoadError("Test error")
    
    def test_raise_fitting_error(self) -> None:
        """Test raising FittingError."""
        with self.assertRaises(FittingError):
            raise FittingError("Test error")
    
    def test_catch_specific_as_base(self) -> None:
        """Test catching specific error as base class."""
        try:
            raise FittingError("Test error")
        except RegressionLabError as e:
            self.assertIsInstance(e, FittingError)
    
    def test_error_message(self) -> None:
        """Test error message is preserved."""
        test_message = "This is a test error message"
        try:
            raise DataValidationError(test_message)
        except DataValidationError as e:
            self.assertEqual(str(e), test_message)


if __name__ == '__main__':
    unittest.main()
