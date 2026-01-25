#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for data_loader module.
"""

import unittest
import sys
from pathlib import Path
import tempfile
import pandas as pd

# Add src to path
src_path = Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(src_path))

from loaders.data_loader import (
    get_project_root,
    prepare_data_path,
    get_variable_names,
    get_file_list_by_type
)
from utils.exceptions import InvalidFileTypeError


class TestGetProjectRoot(unittest.TestCase):
    """Tests for get_project_root function."""
    
    def test_returns_path(self) -> None:
        """Test that function returns a Path object."""
        root = get_project_root()
        self.assertIsInstance(root, Path)
    
    def test_path_exists(self) -> None:
        """Test that returned path exists."""
        root = get_project_root()
        self.assertTrue(root.exists())
    
    def test_has_src_directory(self) -> None:
        """Test that project root contains src directory."""
        root = get_project_root()
        self.assertTrue((root / 'src').exists())


class TestPrepareDataPath(unittest.TestCase):
    """Tests for prepare_data_path function."""
    
    def test_csv_path(self) -> None:
        """Test preparing path for CSV file."""
        path = prepare_data_path('test_file', 'csv')
        self.assertIsInstance(path, str)
        self.assertTrue(path.endswith('.csv'))
        self.assertIn('test_file', path)
    
    def test_xlsx_path(self) -> None:
        """Test preparing path for XLSX file."""
        path = prepare_data_path('test_file', 'xlsx')
        self.assertTrue(path.endswith('.xlsx'))
    
    def test_xls_path(self) -> None:
        """Test preparing path for XLS file."""
        path = prepare_data_path('test_file', 'xls')
        self.assertTrue(path.endswith('.xls'))
    
    def test_custom_base_dir(self) -> None:
        """Test preparing path with custom base directory."""
        path = prepare_data_path('test_file', 'csv', base_dir='custom_dir')
        self.assertIn('custom_dir', path)
    
    def test_absolute_path(self) -> None:
        """Test that returned path is absolute."""
        path = prepare_data_path('test_file', 'csv')
        self.assertTrue(Path(path).is_absolute())


class TestGetVariableNames(unittest.TestCase):
    """Tests for get_variable_names function."""
    
    def test_simple_dataframe(self) -> None:
        """Test getting variable names from simple DataFrame."""
        df = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
        names = get_variable_names(df)
        self.assertEqual(names, ['x', 'y'])
    
    def test_with_uncertainties(self) -> None:
        """Test getting variable names including uncertainties."""
        df = pd.DataFrame({
            'x': [1, 2, 3],
            'ux': [0.1, 0.1, 0.1],
            'y': [4, 5, 6],
            'uy': [0.2, 0.2, 0.2]
        })
        names = get_variable_names(df)
        self.assertEqual(set(names), {'x', 'ux', 'y', 'uy'})
    
    def test_empty_dataframe(self) -> None:
        """Test getting variable names from empty DataFrame."""
        df = pd.DataFrame()
        names = get_variable_names(df)
        self.assertEqual(names, [])
    
    def test_returns_list(self) -> None:
        """Test that function returns a list."""
        df = pd.DataFrame({'a': [1], 'b': [2]})
        names = get_variable_names(df)
        self.assertIsInstance(names, list)


class TestGetFileListByType(unittest.TestCase):
    """Tests for get_file_list_by_type function."""
    
    def setUp(self) -> None:
        """Set up test file lists."""
        self.csv_files = ['file1', 'file2']
        self.xls_files = ['file3']
        self.xlsx_files = ['file4', 'file5', 'file6']
    
    def test_get_csv_files(self) -> None:
        """Test getting CSV file list."""
        result = get_file_list_by_type(
            'csv',
            self.csv_files,
            self.xls_files,
            self.xlsx_files
        )
        self.assertEqual(result, self.csv_files)
    
    def test_get_xls_files(self) -> None:
        """Test getting XLS file list."""
        result = get_file_list_by_type(
            'xls',
            self.csv_files,
            self.xls_files,
            self.xlsx_files
        )
        self.assertEqual(result, self.xls_files)
    
    def test_get_xlsx_files(self) -> None:
        """Test getting XLSX file list."""
        result = get_file_list_by_type(
            'xlsx',
            self.csv_files,
            self.xls_files,
            self.xlsx_files
        )
        self.assertEqual(result, self.xlsx_files)
    
    def test_invalid_file_type(self) -> None:
        """Test invalid file type raises error."""
        with self.assertRaises(InvalidFileTypeError):
            get_file_list_by_type(
                'pdf',
                self.csv_files,
                self.xls_files,
                self.xlsx_files
            )
    
    def test_empty_lists(self) -> None:
        """Test with empty file lists."""
        result = get_file_list_by_type('csv', [], [], [])
        self.assertEqual(result, [])


if __name__ == '__main__':
    unittest.main()
