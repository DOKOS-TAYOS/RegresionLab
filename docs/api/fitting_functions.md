# fitting.fitting_functions

This module contains the mathematical functions used for curve fitting and their corresponding fitting wrapper functions.

## Overview

The module is organized into two types of functions:

1. **Mathematical functions** (`*_function`): Pure mathematical functions that calculate y from x and parameters
2. **Fitting functions** (`fit_*`): Wrapper functions that perform curve fitting and return results

## Mathematical Functions

### Linear Functions

#### `linear_function(t, m)`
Linear function passing through origin: y = mx

**Parameters:**
- `t`: Independent variable (scalar or array)
- `m`: Slope

**Returns:** Calculated y values

---

#### `linear_function_with_n(t, m, n)`
Linear function with intercept: y = mx + n

**Parameters:**
- `t`: Independent variable
- `m`: Slope
- `n`: Y-intercept

**Returns:** Calculated y values

### Polynomial Functions

#### `quadratic_function(t, a)`
Quadratic function: y = ax²

#### `quadratic_function_complete(t, a, b, c)`
Complete quadratic: y = ax² + bx + c

#### `fourth_power(t, a)`
Fourth power: y = ax⁴

### Trigonometric Functions

#### `sin_function(t, a, b)`
Sine function: y = a·sin(bx)

#### `sin_function_with_c(t, a, b, c)`
Sine with phase: y = a·sin(bx + c)

#### `cos_function(t, a, b)`
Cosine function: y = a·cos(bx)

#### `cos_function_with_c(t, a, b, c)`
Cosine with phase: y = a·cos(bx + c)

### Hyperbolic Functions

#### `sinh_function(t, a, b)`
Hyperbolic sine: y = a·sinh(bx)

#### `cosh_function(t, a, b)`
Hyperbolic cosine: y = a·cosh(bx)

### Logarithmic Functions

#### `ln_function(t, a)`
Natural logarithm: y = a·ln(x)

### Inverse Functions

#### `inverse_function(t, a)`
Inverse function: y = a/x

#### `inverse_square_function(t, a)`
Inverse square: y = a/x²

## Fitting Functions

All fitting functions follow the same signature and return format:

```python
def fitting_function(data: dict, x_name: str, y_name: str) -> Tuple[str, np.ndarray, str, float]:
    """
    Fit equation to data.
    
    Args:
        data: Dictionary with x, y, and optional uncertainty arrays
        x_name: Name of independent variable key
        y_name: Name of dependent variable key
        
    Returns:
        Tuple containing:
            - parameter_text: Formatted string of parameters with uncertainties
            - y_fitted: Fitted y values as ndarray
            - equation: Formatted equation string with parameter values
            - r_squared: Coefficient of determination (R²)
    """
```

### Available Fitting Functions

- `fit_linear_function(data, x_name, y_name)` - Fit y = mx
- `fit_linear_function_with_n(data, x_name, y_name)` - Fit y = mx + n
- `fit_quadratic_function(data, x_name, y_name)` - Fit y = ax²
- `fit_quadratic_function_complete(data, x_name, y_name)` - Fit y = ax² + bx + c
- `fit_fourth_power(data, x_name, y_name)` - Fit y = ax⁴
- `fit_sin_function(data, x_name, y_name)` - Fit y = a·sin(bx)
- `fit_sin_function_with_c(data, x_name, y_name)` - Fit y = a·sin(bx + c)
- `fit_cos_function(data, x_name, y_name)` - Fit y = a·cos(bx)
- `fit_cos_function_with_c(data, x_name, y_name)` - Fit y = a·cos(bx + c)
- `fit_sinh_function(data, x_name, y_name)` - Fit y = a·sinh(bx)
- `fit_cosh_function(data, x_name, y_name)` - Fit y = a·cosh(bx)
- `fit_ln_function(data, x_name, y_name)` - Fit y = a·ln(x)
- `fit_inverse_function(data, x_name, y_name)` - Fit y = a/x
- `fit_inverse_square_function(data, x_name, y_name)` - Fit y = a/x²

## Example Usage

```python
import numpy as np
from fitting.fitting_functions import linear_function_with_n, fit_linear_function_with_n

# Generate synthetic data
x = np.linspace(0, 10, 50)
y_true = 2.5 * x + 1.3
y_noisy = y_true + np.random.normal(0, 0.5, 50)

# Create data dictionary
data = {
    'x': x,
    'y': y_noisy,
    'ux': np.ones(50) * 0.1,
    'uy': np.ones(50) * 0.5
}

# Perform fitting
param_text, y_fitted, equation, r_squared = fit_linear_function_with_n(data, 'x', 'y')

print(f"Parameters:\n{param_text}")
print(f"Equation: {equation}")
print(f"R² = {r_squared:.4f}")
```

## Adding New Functions

See [Extending RegressionLab](../extending.md) for a detailed guide on adding new fitting functions.

Quick steps:
1. Define mathematical function (`*_function`)
2. Create fitting wrapper (`fit_*`)
3. Register in `config.py` and `fitting_utils.py`
4. Add translations
5. Test thoroughly

## Technical Details

### Implementation

All fitting functions use `generic_fit()` from `fitting_utils` which wraps `scipy.optimize.curve_fit`. This provides:

- Weighted fitting based on uncertainties
- Automatic covariance matrix calculation
- Parameter uncertainty estimation
- R² calculation

### Numerical Considerations

- Initial parameter guesses improve convergence for nonlinear functions
- Trigonometric functions use FFT-based period estimation
- Bounds can be applied to constrain parameters
- Robust loss functions available for outlier-heavy data

---

*For implementation details, see the source code: `src/fitting/fitting_functions.py`*
