# fitting.workflow_controller

Workflow controller for fitting operations.

## Overview

The `workflow_controller.py` module contains coordination functions and workflow patterns for the fitting application. It orchestrates complex operations like data loading, equation selection, and fitting loops.

## Key Functions

### Data Reloading

#### `reload_data_by_type(file_path: str, file_type: str) -> pd.DataFrame`

Reload data from a file based on its type.

This function is used in loop mode to reload updated data from the same file. Useful when the user is modifying data in real-time and wants to see the updated fit after each modification.

**Parameters:**
- `file_path`: Path to the data file
- `file_type`: Type of file ('csv', 'xlsx', 'txt')

**Returns:**
- Loaded data as DataFrame

**Raises:**
- `DataLoadError`: If file_type is not supported or loading fails

**Example:**
```python
from fitting.workflow_controller import reload_data_by_type

# Reload CSV data
data = reload_data_by_type('input/data.csv', 'csv')
```

### Fitting Loop Workflows

#### `single_fit_with_loop(fitter_function, data, x_name, y_name, plot_name, data_file_path, data_file_type) -> None`

Execute a single fitting operation with optional loop mode.

This function performs an initial fit and then optionally loops, reloading data and refitting each iteration. This is useful for iterative data analysis where the user modifies the data file between fits to explore different scenarios.

**Workflow:**
1. Perform initial fit with current data
2. Show results and ask if user wants to continue
3. If yes: reload data from file and repeat
4. If no: exit

**Parameters:**
- `fitter_function`: Fitting function to call (must accept data, x_name, y_name, plot_name)
- `data`: Initial dataset (pandas DataFrame)
- `x_name`: X variable column name
- `y_name`: Y variable column name
- `plot_name`: Plot name for window titles and filename
- `data_file_path`: Path to data file for reloading
- `data_file_type`: File type ('csv', 'xlsx', 'txt')

**Example:**
```python
from fitting.workflow_controller import single_fit_with_loop
from fitting.fitting_utils import get_fitting_function

fit_func = get_fitting_function('linear_function')
single_fit_with_loop(
    fit_func, data, 'x', 'y', 'my_plot',
    'input/data.csv', 'csv'
)
```

#### `multiple_fit_with_loop(fitter_function, datasets) -> None`

Execute multiple fitting operations with optional loop mode.

Performs fitting on multiple datasets sequentially, with the option to reload and refit each dataset in a loop. Each dataset can be independently continued or stopped.

**Workflow:**
1. Fit all datasets once
2. Ask user for each dataset if they want to continue
3. For datasets marked to continue: reload and refit
4. Repeat until no datasets are marked to continue

**Parameters:**
- `fitter_function`: Fitting function to call
- `datasets`: List of dictionaries, each containing:
  - `'data'`: dataset (pandas DataFrame)
  - `'x_name'`: X variable column name
  - `'y_name'`: Y variable column name
  - `'plot_name'`: plot name for display and filename
  - `'file_path'`: path to data file for reloading
  - `'file_type'`: file type ('csv', 'xlsx', 'txt')

**Example:**
```python
datasets = [
    {
        'data': df1, 'x_name': 'x', 'y_name': 'y',
        'plot_name': 'dataset1', 'file_path': 'data1.csv', 'file_type': 'csv'
    },
    {
        'data': df2, 'x_name': 'time', 'y_name': 'distance',
        'plot_name': 'dataset2', 'file_path': 'data2.csv', 'file_type': 'csv'
    }
]
multiple_fit_with_loop(fit_func, datasets)
```

#### `apply_all_equations(equation_setter, get_fitter, equation_types, data, x_name, y_name, plot_name=None) -> None`

Apply all available equation types to a dataset.

This function automatically tests all predefined equation types on a single dataset, displaying results for each. Useful for exploratory data analysis to determine which mathematical model best fits the data.

**Parameters:**
- `equation_setter`: Function to set the current equation type (e.g., 'linear_function')
- `get_fitter`: Function to retrieve the fitter for the currently set equation type
- `equation_types`: List of equation type identifiers to test
- `data`: Dataset to fit (pandas DataFrame)
- `x_name`: Independent variable column name
- `y_name`: Dependent variable column name
- `plot_name`: Plot name for display and filename (optional)

**Example:**
```python
from config import AVAILABLE_EQUATION_TYPES
from fitting.workflow_controller import apply_all_equations

apply_all_equations(
    equation_setter=my_setter,
    get_fitter=my_getter,
    equation_types=AVAILABLE_EQUATION_TYPES,
    data=df,
    x_name='x',
    y_name='y',
    plot_name='comparison'
)
```

### Data Loading Coordination

#### `coordinate_data_loading(parent_window, ask_file_type_func, ask_file_name_func, ask_variables_func) -> Tuple`

Coordinate the complete data loading workflow.

This function orchestrates the entire data loading process:
1. Get available files
2. Ask user for file type
3. Ask user for specific file
4. Load the data
5. Ask user for variables to use

**Parameters:**
- `parent_window`: Parent Tkinter window
- `ask_file_type_func`: Function to ask for file type
- `ask_file_name_func`: Function to ask for file name
- `ask_variables_func`: Function to ask for variables

**Returns:**
- Tuple: `(data, x_name, y_name, plot_name, file_path, file_type)`
- Returns empty tuple if user cancels

**Example:**
```python
from frontend.ui_dialogs import ask_file_type, ask_file_name, ask_variables
from fitting.workflow_controller import coordinate_data_loading

result = coordinate_data_loading(
    parent_window=root,
    ask_file_type_func=ask_file_type,
    ask_file_name_func=ask_file_name,
    ask_variables_func=ask_variables
)

if result:
    data, x_name, y_name, plot_name, file_path, file_type = result
```

#### `coordinate_data_viewing(parent_window, ask_file_type_func, ask_file_name_func, show_data_func) -> None`

Coordinate the data viewing workflow.

This function orchestrates the process of selecting and displaying data from files without performing any fitting operations.

**Parameters:**
- `parent_window`: Parent Tkinter window
- `ask_file_type_func`: Function to ask for file type
- `ask_file_name_func`: Function to ask for file name
- `show_data_func`: Function to display data

### Equation Selection Coordination

#### `coordinate_equation_selection(parent_window, ask_equation_type_func, ask_num_parameters_func, ask_parameter_names_func, ask_custom_formula_func, get_fitting_function_func) -> Tuple[str, Optional[Callable]]`

Coordinate the equation selection workflow.

Handles the complete process of equation selection, including both predefined equations and custom user-defined equations.

**Parameters:**
- `parent_window`: Parent Tkinter window
- `ask_equation_type_func`: Function to ask for equation type
- `ask_num_parameters_func`: Function to ask for number of parameters
- `ask_parameter_names_func`: Function to ask for parameter names
- `ask_custom_formula_func`: Function to ask for custom formula
- `get_fitting_function_func`: Function to retrieve fitting function by name

**Returns:**
- Tuple of `(equation_name, fitter_function)`

**Example:**
```python
from frontend.ui_dialogs import (
    ask_equation_type, ask_num_parameters, ask_parameter_names,
    ask_custom_formula
)
from fitting.fitting_utils import get_fitting_function
from fitting.workflow_controller import coordinate_equation_selection

eq_name, fit_func = coordinate_equation_selection(
    parent_window=root,
    ask_equation_type_func=ask_equation_type,
    ask_num_parameters_func=ask_num_parameters,
    ask_parameter_names_func=ask_parameter_names,
    ask_custom_formula_func=ask_custom_formula,
    get_fitting_function_func=get_fitting_function
)
```

#### `coordinate_custom_equation(parent_window, ask_num_parameters_func, ask_parameter_names_func, ask_custom_formula_func) -> Tuple[str, Optional[Callable]]`

Coordinate the custom equation creation workflow.

Handles the process of creating a user-defined custom fitting equation by collecting parameter information and the formula.

**Parameters:**
- `parent_window`: Parent Tkinter window
- `ask_num_parameters_func`: Function to ask for number of parameters
- `ask_parameter_names_func`: Function to ask for parameter names
- `ask_custom_formula_func`: Function to ask for custom formula

**Returns:**
- Tuple of `('custom: <formula>', backend_fit_function)` or `(EXIT_SIGNAL, None)` if cancelled

## Usage Patterns

### Single Fit with Loop

```python
from fitting.workflow_controller import single_fit_with_loop
from fitting.fitting_utils import get_fitting_function

# Get fitting function
fit_func = get_fitting_function('linear_function')

# Perform fit with loop capability
single_fit_with_loop(
    fitter_function=fit_func,
    data=dataframe,
    x_name='x',
    y_name='y',
    plot_name='my_fit',
    data_file_path='input/data.csv',
    data_file_type='csv'
)
```

### Multiple Datasets

```python
from fitting.workflow_controller import multiple_fit_with_loop

datasets = [
    {
        'data': df1, 'x_name': 'x', 'y_name': 'y',
        'plot_name': 'dataset1', 'file_path': 'data1.csv', 'file_type': 'csv'
    },
    {
        'data': df2, 'x_name': 'time', 'y_name': 'distance',
        'plot_name': 'dataset2', 'file_path': 'data2.csv', 'file_type': 'csv'
    }
]

multiple_fit_with_loop(fit_func, datasets)
```

### Complete Workflow

```python
from fitting.workflow_controller import (
    coordinate_data_loading,
    coordinate_equation_selection
)
from frontend.ui_dialogs import (
    ask_file_type, ask_file_name, ask_variables,
    ask_equation_type, ask_num_parameters, ask_parameter_names, ask_custom_formula
)
from fitting.fitting_utils import get_fitting_function

# Load data
data_result = coordinate_data_loading(
    parent_window=root,
    ask_file_type_func=ask_file_type,
    ask_file_name_func=ask_file_name,
    ask_variables_func=ask_variables
)

if data_result:
    data, x_name, y_name, plot_name, file_path, file_type = data_result
    
    # Select equation
    eq_name, fit_func = coordinate_equation_selection(
        parent_window=root,
        ask_equation_type_func=ask_equation_type,
        ask_num_parameters_func=ask_num_parameters,
        ask_parameter_names_func=ask_parameter_names,
        ask_custom_formula_func=ask_custom_formula,
        get_fitting_function_func=get_fitting_function
    )
    
    if fit_func:
        # Perform fit
        fit_func(data, x_name, y_name, plot_name)
```

## Best Practices

1. **Error Handling**: Always check return values for empty tuples (user cancellation)
2. **Logging**: The module logs all operations for debugging
3. **User Feedback**: Functions show appropriate dialogs and messages
4. **File Management**: Reload functions handle file errors gracefully

---

*For more information about fitting workflows, see [Usage Guide](../usage.md)*
