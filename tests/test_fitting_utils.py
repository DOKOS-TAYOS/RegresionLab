#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for fitting_utils module.
"""

import unittest
import sys
from pathlib import Path
import numpy as np
import pandas as pd

# Add src to path
# Add src to path
src_path = Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(src_path))

from fitting.fitting_utils import (
    format_parameter,
    generic_fit,
    get_fitting_function,
)
from fitting.estimators import (
    estimate_phase_shift,
    estimate_trigonometric_parameters,
)
from fitting.fitting_functions import linear_function, sin_function
from utils.exceptions import FittingError

class TestFormatParameter(unittest.TestCase):
    """Tests for format_parameter function."""
    
    def test_normal_value(self) -> None:
        """Test formatting normal parameter value."""
        value, sigma = format_parameter(1.234567, 0.001)
        self.assertIsInstance(value, float)
        self.assertIsInstance(sigma, str)
    
    def test_infinite_sigma(self) -> None:
        """Test formatting with infinite uncertainty."""
        value, sigma = format_parameter(1.0, np.inf)
        self.assertEqual(sigma, '∞')
    
    def test_nan_sigma(self) -> None:
        """Test formatting with NaN uncertainty."""
        value, sigma = format_parameter(1.0, np.nan)
        self.assertEqual(sigma, 'NaN')
    
    def test_small_sigma(self) -> None:
        """Test formatting with very small uncertainty."""
        value, sigma = format_parameter(1.23456789, 1e-8)
        self.assertIn('E', sigma)
    
    def test_large_value(self) -> None:
        """Test formatting large parameter value."""
        value, sigma = format_parameter(1234567.89, 100.0)
        self.assertIsInstance(value, float)


class TestEstimateTrigonometricParameters(unittest.TestCase):
    """Tests for estimate_trigonometric_parameters function."""
    
    def test_simple_sine_wave(self) -> None:
        """Test parameter estimation for simple sine wave."""
        x = np.linspace(0, 4*np.pi, 100)
        y = 2.0 * np.sin(x)
        
        amplitude, frequency = estimate_trigonometric_parameters(x, y)
        
        self.assertIsInstance(amplitude, float)
        self.assertIsInstance(frequency, float)
        self.assertGreater(amplitude, 0)
        self.assertGreater(frequency, 0)
    
    def test_cosine_wave(self) -> None:
        """Test parameter estimation for cosine wave."""
        x = np.linspace(0, 4*np.pi, 100)
        y = 3.0 * np.cos(2.0*x)
        
        amplitude, frequency = estimate_trigonometric_parameters(x, y)
        
        self.assertGreater(amplitude, 0)
        self.assertGreater(frequency, 0)
    
    def test_constant_data(self) -> None:
        """Test parameter estimation with constant data."""
        x = np.linspace(0, 10, 50)
        y = np.ones_like(x) * 5.0
        
        amplitude, frequency = estimate_trigonometric_parameters(x, y)
        
        # Should return default values
        self.assertIsInstance(amplitude, float)
        self.assertIsInstance(frequency, float)
    
    def test_noisy_data(self) -> None:
        """Test parameter estimation with noisy data."""
        x = np.linspace(0, 4*np.pi, 100)
        y = 2.0 * np.sin(x) + np.random.normal(0, 0.1, len(x))
        
        amplitude, frequency = estimate_trigonometric_parameters(x, y)
        
        self.assertGreater(amplitude, 0)
        self.assertGreater(frequency, 0)


class TestEstimatePhaseShift(unittest.TestCase):
    """Tests for estimate_phase_shift function."""
    
    def test_phase_estimation(self) -> None:
        """Test phase shift estimation."""
        x = np.linspace(0, 4*np.pi, 100)
        y = 2.0 * np.sin(x + np.pi/4)
        
        phase = estimate_phase_shift(x, y, 2.0, 1.0)
        
        self.assertIsInstance(phase, float)
        self.assertGreaterEqual(phase, -np.pi)
        self.assertLessEqual(phase, np.pi)
    
    def test_zero_amplitude(self) -> None:
        """Test phase estimation with zero amplitude."""
        x = np.linspace(0, 4*np.pi, 100)
        y = np.zeros_like(x)
        
        phase = estimate_phase_shift(x, y, 0.0, 1.0)
        
        self.assertIsInstance(phase, float)


class TestGenericFit(unittest.TestCase):
    """Tests for generic_fit function."""
    
    def setUp(self) -> None:
        """Set up test data."""
        self.x = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        self.y = 2.0 * self.x
        self.ux = np.ones_like(self.x) * 0.1
        self.uy = np.ones_like(self.y) * 0.2
        
        # Create DataFrame instead of dict for validation
        self.data = pd.DataFrame({
            'x': self.x,
            'ux': self.ux,
            'y': self.y,
            'uy': self.uy
        })
    
    def test_linear_fit(self) -> None:
        """Test generic fit with linear function."""
        text, y_fitted, equation = generic_fit(
            self.data,
            'x',
            'y',
            linear_function,
            ['m'],
            'y={m}x'
        )
        
        self.assertIsInstance(text, str)
        # y_fitted can be ndarray or pandas Series
        self.assertTrue(isinstance(y_fitted, (np.ndarray, pd.Series)))
        self.assertIsInstance(equation, str)
        self.assertIn('m=', text)
        self.assertIn('R²=', text)
    
    def test_fit_with_initial_guess(self) -> None:
        """Test generic fit with initial parameter guess."""
        text, y_fitted, equation = generic_fit(
            self.data,
            'x',
            'y',
            linear_function,
            ['m'],
            'y={m}x',
            initial_guess=[1.5]
        )
        
        self.assertIsInstance(text, str)
        self.assertIn('m=', text)
        self.assertIn('R²=', text)
    
    def test_invalid_data(self) -> None:
        """Test generic fit with invalid data."""
        bad_data = pd.DataFrame({
            'x': np.array([1.0, 2.0]),
            'ux': np.array([0.1, 0.1])
        })
        
        with self.assertRaises(FittingError):
            generic_fit(
                bad_data,
                'x',
                'y',
                linear_function,
                ['m'],
                'y={m}x'
            )
    
    def test_non_convergent_fit(self) -> None:
        """Test handling of non-convergent fit."""
        # Create data that's hard to fit with sine
        bad_data = pd.DataFrame({
            'x': np.array([1.0, 2.0, 3.0]),
            'ux': np.array([0.1, 0.1, 0.1]),
            'y': np.array([100.0, 200.0, 300.0]),
            'uy': np.array([1.0, 1.0, 1.0])
        })
        
        # This might raise FittingError if it can't converge
        try:
            generic_fit(
                bad_data,
                'x',
                'y',
                sin_function,
                ['a', 'b'],
                'y={a}sin({b}x)'
            )
        except FittingError:
            pass


class TestGetFittingFunction(unittest.TestCase):
    """Tests for get_fitting_function."""
    
    def test_get_linear_function(self) -> None:
        """Test getting linear fitting function."""
        func = get_fitting_function('linear_function')
        self.assertIsNotNone(func)
        self.assertTrue(callable(func))
    
    def test_get_quadratic_function(self) -> None:
        """Test getting quadratic fitting function."""
        func = get_fitting_function('quadratic_function')
        self.assertIsNotNone(func)
        self.assertTrue(callable(func))
    
    def test_get_sin_function(self) -> None:
        """Test getting sine fitting function."""
        func = get_fitting_function('sin_function')
        self.assertIsNotNone(func)
        self.assertTrue(callable(func))
    
    def test_unknown_equation(self) -> None:
        """Test getting unknown equation returns None."""
        func = get_fitting_function('unknown_equation')
        self.assertIsNone(func)
    
    def test_exit_signal(self) -> None:
        """Test exit signal returns None."""
        from config import EXIT_SIGNAL
        func = get_fitting_function(EXIT_SIGNAL)
        self.assertIsNone(func)


if __name__ == '__main__':
    unittest.main()
