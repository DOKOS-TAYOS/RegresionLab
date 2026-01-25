#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for custom_function_evaluator module.
"""

import unittest
import sys
from pathlib import Path
import numpy as np
import pandas as pd

# Add src to path
src_path = Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(src_path))

from fitting.custom_function_evaluator import CustomFunctionEvaluator
from utils.exceptions import EquationError, ValidationError


class TestCustomFunctionEvaluatorInit(unittest.TestCase):
    """Tests for CustomFunctionEvaluator initialization."""
    
    def test_simple_linear_function(self) -> None:
        """Test creating evaluator with simple linear function."""
        evaluator = CustomFunctionEvaluator("a*x + b", ["a", "b"])
        self.assertIsNotNone(evaluator)
        self.assertEqual(evaluator.parameter_names, ["a", "b"])
    
    def test_quadratic_function(self) -> None:
        """Test creating evaluator with quadratic function."""
        evaluator = CustomFunctionEvaluator("a*x**2 + b*x + c", ["a", "b", "c"])
        self.assertIsNotNone(evaluator)
        self.assertEqual(len(evaluator.parameter_names), 3)
    
    def test_empty_equation(self) -> None:
        """Test that empty equation raises ValidationError."""
        with self.assertRaises(ValidationError):
            CustomFunctionEvaluator("", ["a"])
    
    def test_whitespace_only_equation(self) -> None:
        """Test that whitespace-only equation raises ValidationError."""
        with self.assertRaises(ValidationError):
            CustomFunctionEvaluator("   ", ["a"])
    
    def test_invalid_parameter_names(self) -> None:
        """Test that invalid parameter names raise ValidationError."""
        with self.assertRaises(ValidationError):
            CustomFunctionEvaluator("a*x", ["123invalid"])
    
    def test_duplicate_parameter_names(self) -> None:
        """Test that duplicate parameter names raise ValidationError."""
        with self.assertRaises(ValidationError):
            CustomFunctionEvaluator("a*x + a", ["a", "a"])


class TestPrepareFormula(unittest.TestCase):
    """Tests for formula preparation."""
    
    def test_ln_function_replacement(self) -> None:
        """Test that ln is replaced with np.log."""
        evaluator = CustomFunctionEvaluator("a*ln(x)", ["a"])
        self.assertIn("np.log", evaluator.equation_str)
    
    def test_sin_function_replacement(self) -> None:
        """Test that sin is replaced with np.sin."""
        evaluator = CustomFunctionEvaluator("a*sin(x)", ["a"])
        self.assertIn("np.sin", evaluator.equation_str)
    
    def test_cos_function_replacement(self) -> None:
        """Test that cos is replaced with np.cos."""
        evaluator = CustomFunctionEvaluator("a*cos(x)", ["a"])
        self.assertIn("np.cos", evaluator.equation_str)
    
    def test_exp_function_replacement(self) -> None:
        """Test that exp is replaced with np.exp."""
        evaluator = CustomFunctionEvaluator("a*exp(x)", ["a"])
        self.assertIn("np.exp", evaluator.equation_str)
    
    def test_multiple_replacements(self) -> None:
        """Test multiple function replacements."""
        evaluator = CustomFunctionEvaluator("a*sin(x) + b*cos(x)", ["a", "b"])
        self.assertIn("np.sin", evaluator.equation_str)
        self.assertIn("np.cos", evaluator.equation_str)


class TestFunctionCreation(unittest.TestCase):
    """Tests for function creation."""
    
    def test_linear_function_evaluation(self) -> None:
        """Test that created function evaluates correctly for linear case."""
        evaluator = CustomFunctionEvaluator("a*x + b", ["a", "b"])
        func = evaluator.get_function()
        
        x = np.array([1.0, 2.0, 3.0])
        result = func(x, 2.0, 3.0)
        expected = 2.0 * x + 3.0
        
        np.testing.assert_array_almost_equal(result, expected)
    
    def test_quadratic_function_evaluation(self) -> None:
        """Test that created function evaluates correctly for quadratic case."""
        evaluator = CustomFunctionEvaluator("a*x**2", ["a"])
        func = evaluator.get_function()
        
        x = np.array([1.0, 2.0, 3.0])
        result = func(x, 2.0)
        expected = 2.0 * x**2
        
        np.testing.assert_array_almost_equal(result, expected)
    
    def test_exponential_function_evaluation(self) -> None:
        """Test evaluation with exponential function."""
        evaluator = CustomFunctionEvaluator("a*exp(b*x)", ["a", "b"])
        func = evaluator.get_function()
        
        x = np.array([0.0, 1.0, 2.0])
        result = func(x, 1.0, 0.5)
        expected = 1.0 * np.exp(0.5 * x)
        
        np.testing.assert_array_almost_equal(result, expected)
    
    def test_trigonometric_function_evaluation(self) -> None:
        """Test evaluation with trigonometric function."""
        evaluator = CustomFunctionEvaluator("a*sin(b*x)", ["a", "b"])
        func = evaluator.get_function()
        
        x = np.array([0.0, np.pi/2, np.pi])
        result = func(x, 2.0, 1.0)
        expected = 2.0 * np.sin(1.0 * x)
        
        np.testing.assert_array_almost_equal(result, expected)
    
    def test_wrong_parameter_count(self) -> None:
        """Test that wrong number of parameters raises error."""
        evaluator = CustomFunctionEvaluator("a*x + b", ["a", "b"])
        func = evaluator.get_function()
        
        x = np.array([1.0, 2.0, 3.0])
        with self.assertRaises(EquationError):
            func(x, 2.0)  # Missing one parameter
    
    def test_division_by_zero(self) -> None:
        """Test that division by zero produces inf/nan values."""
        evaluator = CustomFunctionEvaluator("a/x", ["a"])
        func = evaluator.get_function()
        
        x = np.array([0.0, 1.0, 2.0])
        # Suppress the division by zero warning from NumPy
        with np.errstate(divide='ignore', invalid='ignore'):
            result = func(x, 1.0)
        self.assertTrue(np.isinf(result[0]) or np.isnan(result[0]))


class TestEquationTemplate(unittest.TestCase):
    """Tests for equation template generation."""
    
    def test_simple_template(self) -> None:
        """Test template generation for simple equation."""
        evaluator = CustomFunctionEvaluator("a*x + b", ["a", "b"])
        template = evaluator._generate_equation_template()
        
        self.assertIn("{a}", template)
        self.assertIn("{b}", template)
        self.assertTrue(template.startswith("y="))
    
    def test_complex_template(self) -> None:
        """Test template generation for complex equation."""
        evaluator = CustomFunctionEvaluator("a*sin(b*x + c)", ["a", "b", "c"])
        template = evaluator._generate_equation_template()
        
        self.assertIn("{a}", template)
        self.assertIn("{b}", template)
        self.assertIn("{c}", template)
        self.assertTrue(template.startswith("y="))


class TestFitMethod(unittest.TestCase):
    """Tests for the fit method."""
    
    def setUp(self) -> None:
        """Set up test data."""
        self.x = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        self.y = 2.0 * self.x + 1.0
        self.ux = np.ones_like(self.x) * 0.1
        self.uy = np.ones_like(self.y) * 0.2
        
        self.data = pd.DataFrame({
            'x': self.x,
            'ux': self.ux,
            'y': self.y,
            'uy': self.uy
        })
    
    def test_fit_initialization(self) -> None:
        """Test that CustomFunctionEvaluator initializes correctly for fitting."""
        evaluator = CustomFunctionEvaluator("a*x + b", ["a", "b"])
        
        self.assertIsNotNone(evaluator.function)
        self.assertEqual(evaluator.parameter_names, ["a", "b"])
        self.assertEqual(evaluator.original_equation_str, "a*x + b")
    
    def test_get_function_callable(self) -> None:
        """Test that get_function returns a callable."""
        evaluator = CustomFunctionEvaluator("a*x", ["a"])
        func = evaluator.get_function()
        
        self.assertTrue(callable(func))
        # Test that function can be called
        x = np.array([1.0, 2.0, 3.0])
        result = func(x, 2.0)
        expected = 2.0 * x
        np.testing.assert_array_almost_equal(result, expected)


class TestReprMethod(unittest.TestCase):
    """Tests for string representation."""
    
    def test_repr(self) -> None:
        """Test string representation of evaluator."""
        evaluator = CustomFunctionEvaluator("a*x + b", ["a", "b"])
        repr_str = repr(evaluator)
        
        self.assertIn("CustomFunctionEvaluator", repr_str)
        self.assertIn("a*x + b", repr_str)
        self.assertIn("a", repr_str)
        self.assertIn("b", repr_str)


if __name__ == '__main__':
    unittest.main()
