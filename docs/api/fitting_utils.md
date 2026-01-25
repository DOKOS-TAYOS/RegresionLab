# fitting.fitting_utils

Utility functions for curve fitting operations.

## Overview

This module provides the core fitting utilities used by all fitting functions in RegressionLab. It abstracts the underlying optimization library (SciPy by default) and provides helper functions for parameter estimation.

## Core Functions

### Fitting Operations

#### `generic_fit(data: dict, x_name: str, y_name: str, fit_func: Callable, param_names: List[str], equation_template: str, initial_guess: Optional[List[float]] = None) -> Tuple[str, NDArray, str, float]`

The main fitting function used by all equation-specific fitters.

Generic curve fitting using `scipy.optimize.curve_fit`. This function handles weighted fitting based on uncertainties, calculates parameter uncertainties, and computes R².

**Parameters:**
- `data`: Data dictionary containing x, y and their uncertainties
- `x_name`: Name of the x variable
- `y_name`: Name of the y variable
- `fit_func`: Function to fit (e.g., `linear_function_with_n`, `sin_function`, etc.)
- `param_names`: List of parameter names (e.g., `['m', 'n']` or `['a', 'b', 'c']`)
- `equation_template`: Template for equation display (e.g., `"y={m}x+{n}"`)
- `initial_guess`: Optional initial parameter values for fitting (improves convergence)

**Returns:**
- Tuple containing:
  - `text`: Formatted text with parameters and uncertainties
  - `y_fitted`: Array with fitted y values
  - `equation`: Formatted equation with parameter values
  - `r_squared`: Coefficient of determination (R²)

**Raises:**
- `FittingError`: If `curve_fit` fails to converge

**Example:**
```python
from fitting.fitting_utils import generic_fit
from fitting.fitting_functions import linear_function_with_n
import numpy as np

# Create data dictionary
data = {
    'x': np.array([1, 2, 3, 4, 5]),
    'y': np.array([2.5, 5.1, 7.4, 10.2, 12.6]),
    'ux': np.ones(5) * 0.1,
    'uy': np.ones(5) * 0.5
}

text, y_fitted, equation, r_squared = generic_fit(
    data, 'x', 'y',
    fit_func=linear_function_with_n,
    param_names=['m', 'n'],
    equation_template='y={m}x+{n}'
)
print(f"Parameters:\n{text}")
print(f"Equation: {equation}")
print(f"R² = {r_squared:.4f}")
```

#### `get_fitting_function(equation_name: str) -> Optional[Callable]`

Factory function that returns the appropriate fitting function for a given equation name.

**Parameters:**
- `equation_name`: Name from `config.EQUATION_FUNCTION_MAP` (e.g., 'linear_function_with_n')

**Returns:**
- Fitting function (e.g., `fit_linear_function_with_n`) or `None` if not found

**Example:**
```python
from fitting.fitting_utils import get_fitting_function

# Get fitting function by name
fit_func = get_fitting_function('linear_function_with_n')

# Use it to fit data
param_text, y_fitted, equation, r2 = fit_func(data, 'x', 'y')
```

## Helper Functions

### Parameter Estimation

#### `estimate_trigonometric_parameters(x: NDArray, y: NDArray) -> Tuple[float, float]`

Estimates initial parameters for trigonometric functions using peak detection.

This function estimates the amplitude (a) and angular frequency (b) for functions of the form: `y = a * sin(b*x)` or `y = a * cos(b*x)`. Uses peak detection to estimate the period and calculates frequency from it.

**Parameters:**
- `x`: Independent variable array
- `y`: Dependent variable array

**Returns:**
- Tuple of `(amplitude, frequency)`:
  - `amplitude`: Estimated amplitude parameter (a)
  - `frequency`: Estimated angular frequency parameter (b)

#### `estimate_phase_shift(x: np.ndarray, y: np.ndarray, amplitude: float, frequency: float) -> float`

Estimates phase shift for trigonometric functions.

**Parameters:**
- `x`: Independent variable
- `y`: Dependent variable
- `amplitude`: Known amplitude
- `frequency`: Known frequency

**Returns:**
- Estimated phase shift (c parameter)

## Statistical Functions

### R² Calculation

The coefficient of determination (R²) is calculated as:

```python
r_squared = 1 - (SS_res / SS_tot)

where:
    SS_res = Σ(y - y_fitted)²  # Residual sum of squares
    SS_tot = Σ(y - ȳ)²         # Total sum of squares
```

**Interpretation:**
- R² = 1.0: Perfect fit
- R² > 0.95: Excellent fit
- R² > 0.85: Good fit
- R² > 0.70: Acceptable fit
- R² < 0.70: Poor fit

### Weighted Fitting

When uncertainties are provided in the data dictionary:

```python
# Data dictionary includes uncertainties
data = {
    'x': x_array,
    'y': y_array,
    'ux': x_uncertainties,  # Optional
    'uy': y_uncertainties   # Used as weights
}

# generic_fit automatically extracts and uses uy as sigma
# SciPy curve_fit uses these as sigma
popt, pcov = curve_fit(fit_func, x, y, sigma=uy, absolute_sigma=True)
```

This gives more weight to data points with smaller uncertainties, which is statistically correct for experimental data.

## Advanced Usage

### Custom Initial Guesses

For complex functions, providing good initial guesses improves convergence:

```python
# Example: Gaussian function
def fit_gaussian_with_guess(data, x_name, y_name):
    x = data[x_name]
    y = data[y_name]
    
    # Estimate initial parameters
    a0 = np.max(y)                    # Amplitude
    mu0 = x[np.argmax(y)]             # Center
    sigma0 = (np.max(x) - np.min(x)) / 4  # Width
    
    initial_guess = [a0, mu0, sigma0]
    
    text, y_fitted, equation, r_squared = generic_fit(
        data, x_name, y_name,
        fit_func=gaussian_function,
        param_names=['a', 'mu', 'sigma'],
        equation_template='y={a}*exp(-((x-{mu})/{sigma})^2)',
        initial_guess=initial_guess
    )
    ...
```

### Replacing the Backend

To use a different optimization library, modify `generic_fit()`:

```python
def generic_fit_custom(data, x_name, y_name, fit_func, param_names, equation_template, initial_guess=None):
    """Custom fitting using alternative library."""
    # Import your preferred library
    from alternative_lib import fit_function
    
    # Extract data
    x = data[x_name]
    y = data[y_name]
    uy = data.get(f'u{y_name}', None)
    
    # Perform fit
    result = fit_function(fit_func, x, y, weights=uy, initial=initial_guess)
    
    # Extract results
    params = result.parameters
    y_fitted = fit_func(x, *params)
    r_squared = calculate_r_squared(y, y_fitted)
    
    # Format output (similar to original generic_fit)
    text = format_parameters(param_names, params, result.uncertainties)
    equation = equation_template.format(**dict(zip(param_names, params)))
    
    return text, y_fitted, equation, r_squared
```

See [Customizing the Fitting Core](../customization.md) for details.

## Error Handling

The fitting utilities raise specific exceptions:

```python
from utils.exceptions import FittingError
from fitting.fitting_utils import generic_fit
from fitting.fitting_functions import linear_function_with_n

try:
    text, y_fitted, equation, r_squared = generic_fit(
        data, 'x', 'y',
        fit_func=linear_function_with_n,
        param_names=['m', 'n'],
        equation_template='y={m}x+{n}'
    )
except FittingError as e:
    print(f"Fitting failed: {e}")
    # Handle error (try different equation, initial guess, etc.)
```

Common causes of fitting failures:
- Insufficient data points
- Poor initial guess
- Wrong equation for data
- Numerical issues (infinity, NaN values)

---

*For more details, see source code: `src/fitting/fitting_utils.py`*
