#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for workflow_controller module.
"""

import unittest
import sys
from pathlib import Path
import tempfile
import pandas as pd

# Add src to path
src_path = Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(src_path))

from fitting.workflow_controller import (
    reload_data_by_type,
    apply_all_equations
)
from utils.exceptions import DataLoadError


class TestReloadDataByType(unittest.TestCase):
    """Tests for reload_data_by_type function."""
    
    def setUp(self) -> None:
        """Create temporary data file."""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx')
        self.temp_file.close()
        
        df = pd.DataFrame({
            'x': [1.0, 2.0, 3.0],
            'y': [2.0, 4.0, 6.0]
        })
        df.to_excel(self.temp_file.name, index=False)
    
    def tearDown(self) -> None:
        """Remove temporary file."""
        Path(self.temp_file.name).unlink(missing_ok=True)
    
    def test_reload_xlsx(self) -> None:
        """Test reloading XLSX file."""
        df = reload_data_by_type(self.temp_file.name, 'xlsx')
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 3)
    
    def test_invalid_file_type(self) -> None:
        """Test reloading with invalid file type raises error."""
        with self.assertRaises(DataLoadError):
            reload_data_by_type(self.temp_file.name, 'invalid')
    
    def test_nonexistent_file(self) -> None:
        """Test reloading nonexistent file raises error."""
        with self.assertRaises(Exception):
            reload_data_by_type('/nonexistent/file.xlsx', 'xlsx')


class TestApplyAllEquations(unittest.TestCase):
    """Tests for apply_all_equations function."""
    
    def setUp(self) -> None:
        """Set up test data and tracking."""
        self.data = pd.DataFrame({
            'x': [1.0, 2.0, 3.0],
            'ux': [0.1, 0.1, 0.1],
            'y': [2.0, 4.0, 6.0],
            'uy': [0.2, 0.2, 0.2]
        })
        
        self.current_equation = None
        self.fit_calls = []
    
    def equation_setter(self, eq_type: str) -> None:
        """Mock equation setter."""
        self.current_equation = eq_type
    
    def get_fitter(self):
        """Mock fitter getter."""
        def mock_fitter(data, x_name, y_name, plot_name):
            self.fit_calls.append({
                'equation': self.current_equation,
                'x_name': x_name,
                'y_name': y_name,
                'plot_name': plot_name
            })
        return mock_fitter
    
    def test_apply_multiple_equations(self) -> None:
        """Test applying multiple equations."""
        equation_types = ['eq1', 'eq2', 'eq3']
        
        apply_all_equations(
            equation_setter=self.equation_setter,
            get_fitter=self.get_fitter,
            equation_types=equation_types,
            data=self.data,
            x_name='x',
            y_name='y',
            plot_name='test_plot'
        )
        
        # Check that all equations were applied
        self.assertEqual(len(self.fit_calls), 3)
        
        # Check equation names
        applied_equations = [call['equation'] for call in self.fit_calls]
        self.assertEqual(applied_equations, equation_types)
    
    def test_apply_with_plot_name(self) -> None:
        """Test applying equations with plot name."""
        equation_types = ['eq1']
        
        apply_all_equations(
            equation_setter=self.equation_setter,
            get_fitter=self.get_fitter,
            equation_types=equation_types,
            data=self.data,
            x_name='x',
            y_name='y',
            plot_name='my_plot'
        )
        
        # Check plot name includes equation type
        self.assertIn('my_plot_eq1', self.fit_calls[0]['plot_name'])
    
    def test_apply_empty_list(self) -> None:
        """Test applying empty equation list."""
        apply_all_equations(
            equation_setter=self.equation_setter,
            get_fitter=self.get_fitter,
            equation_types=[],
            data=self.data,
            x_name='x',
            y_name='y',
            plot_name='test_plot'
        )
        
        # No fits should be called
        self.assertEqual(len(self.fit_calls), 0)


if __name__ == '__main__':
    unittest.main()
