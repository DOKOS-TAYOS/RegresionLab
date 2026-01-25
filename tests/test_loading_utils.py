#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for loading_utils module.
"""

import unittest
import sys
from pathlib import Path
import tempfile
import pandas as pd
import csv

# Add src to path
src_path = Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(src_path))

from loaders.loading_utils import csv_reader, excel_reader
from utils.exceptions import DataLoadError


class TestCsvReader(unittest.TestCase):
    """Tests for csv_reader function."""
    
    def setUp(self) -> None:
        """Create temporary CSV file for testing."""
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv')
        writer = csv.writer(self.temp_file)
        writer.writerow(['x', 'ux', 'y', 'uy'])
        writer.writerow([1.0, 0.1, 2.0, 0.2])
        writer.writerow([2.0, 0.1, 4.0, 0.2])
        writer.writerow([3.0, 0.1, 6.0, 0.2])
        self.temp_file.close()
    
    def tearDown(self) -> None:
        """Remove temporary file."""
        Path(self.temp_file.name).unlink(missing_ok=True)
    
    def test_read_valid_csv(self) -> None:
        """Test reading valid CSV file."""
        df = csv_reader(self.temp_file.name)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 3)
        self.assertIn('x', df.columns)
        self.assertIn('y', df.columns)
    
    def test_nonexistent_file(self) -> None:
        """Test reading nonexistent file raises error."""
        with self.assertRaises(DataLoadError):
            csv_reader('/nonexistent/file.csv')
    
    def test_returns_dataframe(self) -> None:
        """Test that function returns DataFrame."""
        df = csv_reader(self.temp_file.name)
        self.assertIsInstance(df, pd.DataFrame)


class TestExcelReader(unittest.TestCase):
    """Tests for excel_reader function."""
    
    def setUp(self) -> None:
        """Create temporary Excel file for testing."""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx')
        self.temp_file.close()
        
        df = pd.DataFrame({
            'x': [1.0, 2.0, 3.0],
            'ux': [0.1, 0.1, 0.1],
            'y': [2.0, 4.0, 6.0],
            'uy': [0.2, 0.2, 0.2]
        })
        df.to_excel(self.temp_file.name, index=False)
    
    def tearDown(self) -> None:
        """Remove temporary file."""
        Path(self.temp_file.name).unlink(missing_ok=True)
    
    def test_read_valid_excel(self) -> None:
        """Test reading valid Excel file."""
        df = excel_reader(self.temp_file.name)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 3)
        self.assertIn('x', df.columns)
        self.assertIn('y', df.columns)
    
    def test_nonexistent_file(self) -> None:
        """Test reading nonexistent file raises error."""
        with self.assertRaises(DataLoadError):
            excel_reader('/nonexistent/file.xlsx')
    
    def test_returns_dataframe(self) -> None:
        """Test that function returns DataFrame."""
        df = excel_reader(self.temp_file.name)
        self.assertIsInstance(df, pd.DataFrame)


if __name__ == '__main__':
    unittest.main()
