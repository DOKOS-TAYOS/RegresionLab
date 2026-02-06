"""Application constants, equation mappings, and version."""

from pathlib import Path
from typing import Any

import yaml

# Application version number
__version__ = "0.8.3"

# ---------------------------------------------------------------------------
# Equations: single source of truth from YAML
# Each entry has: function (fit function name), formula (display), param_names (list)
# ---------------------------------------------------------------------------

_EQUATIONS_PATH = Path(__file__).resolve().parent / "equations.yaml"

with open(_EQUATIONS_PATH, encoding="utf-8") as _f:
    _raw_equations: dict[str, Any] = yaml.safe_load(_f)

# Single source of truth: eq_id -> { function, formula, param_names }
# Use EQUATIONS[eq_id]["function"], EQUATIONS[eq_id]["formula"], EQUATIONS[eq_id]["param_names"]
EQUATIONS: dict[str, dict[str, Any]] = _raw_equations
AVAILABLE_EQUATION_TYPES: list[str] = list(EQUATIONS.keys())

# ---------------------------------------------------------------------------
# Other constants
# ---------------------------------------------------------------------------

# Regular expression patterns for replacing mathematical function names
# with their NumPy equivalents when parsing user-defined equations
MATH_FUNCTION_REPLACEMENTS: dict[str, str] = {
    r'\bln\b': 'np.log',
    r'\bsin\b': 'np.sin',
    r'\bcos\b': 'np.cos',
    r'\btan\b': 'np.tan',
    r'\bsinh\b': 'np.sinh',
    r'\bcosh\b': 'np.cosh',
    r'\btanh\b': 'np.tanh',
    r'\bexp\b': 'np.exp',
    r'\bsqrt\b': 'np.sqrt',
    r'\babs\b': 'np.abs',
    r'\bpi\b': 'np.pi',
    r'\be\b': 'np.e',
}

# Central list of supported data file types (extensions without dot).
# All parts of the application (validators, loaders, frontends) should
# reference this constant instead of hardcoding ['csv', 'xlsx', 'txt'].
DATA_FILE_TYPES: tuple[str, ...] = ('csv', 'xlsx', 'txt')

# Signal value used to indicate user wants to exit the application
EXIT_SIGNAL: str = 'Salir'
