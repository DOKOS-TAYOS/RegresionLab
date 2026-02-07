# Streamlit Guide

This guide covers the web-based interface of RegressionLab built with Streamlit. The Streamlit version provides a modern, browser-based experience for curve fitting operations.

## Overview

The Streamlit interface offers:
- **Modern UI**: Clean, intuitive design
- **Accessibility**: Works on any device with a browser
- **No installation**: Use the online version instantly
- **Visual feedback**: Real-time updates and progress indicators
- **Easy sharing**: Share results by downloading plots

## Accessing Streamlit

### Online Version (Recommended)

Visit: [https://regressionlab.streamlit.app/](https://regressionlab.streamlit.app/)

**First-time access**:
1. Open the URL in your browser
2. If you see "App is sleeping", click "Start"
3. Wait 30-60 seconds for the app to wake up
4. The app will load and be ready to use

### Local Version

If you have RegressionLab installed locally:

**Windows:**
```batch
bin\run_streamlit.bat
```

**macOS/Linux:**
```bash
./bin/run_streamlit.sh
```

**Or use the direct command:**
```bash
streamlit run src/streamlit_app/app.py
```

The app will open automatically in your default browser at `http://localhost:8501`.

## Interface Layout

The Streamlit interface consists of three main areas:

### 1. Sidebar (Left)
- **Language Toggle**: Switch between English and Spanish
- **Mode Selection**: Choose your operation mode
  - Normal Fitting
  - Multiple Datasets
  - Checker Fitting
  - Total Fitting

### 2. Main Area (Center)
- **Logo and Title**: RegressionLab branding
- **Help Section**: Expandable information about the app
- **Operation Controls**: File upload, variable selection, equation selection
- **Results Display**: Plots and fitting results

### 3. Results Section (Bottom)
- **Plot Display**: Visualization of fitted curves
- **Parameter Values**: Fitted parameters with uncertainties
- **Download Buttons**: Save plots to your computer

## Language Selection

### Changing the Language

1. Look at the sidebar (left side)
2. Click the language toggle button:
   - "English 🇬🇧" to switch to English
   - "Español 🇪🇸" to switch to Spanish
3. The entire interface updates immediately

**Available Languages**:
- Spanish (Español) - Default
- English

## Operation Modes

### Mode 1: Normal Fitting

**Purpose**: Fit one equation to one dataset

**Steps**:

1. **Select Mode**:
   - In the sidebar, ensure "Normal Fitting" is selected

2. **Upload Data**:
   - Click "Browse files" or drag and drop your file
   - Supported formats: CSV, XLSX, TXT
   - Wait for the file to upload and process

3. **View Data** (Optional):
   - Expand "Show Data" to preview your dataset
   - Verify columns are loaded correctly

4. **Select Variables**:
   - **Independent Variable (X)**: Choose from dropdown (e.g., "time")
   - **Dependent Variable (Y)**: Choose from dropdown (e.g., "temperature")
   - **Plot Name**: Enter a name for the output file (e.g., "experiment1")

5. **Select Equation**:
   - Choose an equation type from the dropdown
   - Options include Linear, Quadratic, Sine, Cosine, Logarithmic, etc.
   - Formula shown next to each option (e.g., "Linear with intercept - y=mx+n")

6. **Fit the Curve**:
   - Click "Normal Fitting" button (blue button)
   - Wait for processing (spinner appears)
   - Results appear below

7. **Review Results**:
   - **Equation**: Mathematical formula with fitted parameters
   - **Parameters**: Values with uncertainties (e.g., "m = 5.12 ± 0.05")
   - **Plot**: Visualization with your data points and fitted curve
   - **R² value**: Goodness of fit measure

8. **Download Plot**:
   - Click the "📥 Download" button
   - Plot saved as PNG image to your downloads folder

**Custom Formula**:

If "Custom Formula" is selected:

1. **Enter Number of Parameters**: Use the number input (1-10)
2. **Name Parameters**: Enter names in the input boxes (e.g., "a", "b", "c")
3. **Enter Formula**: Type your formula using Python syntax
   - Example: `a*x**2 + b*x + c`
   - Use `x` as the independent variable
   - Use parameter names defined above
   - Supported: `+`, `-`, `*`, `/`, `**` (power), `np.sin()`, `np.cos()`, `np.exp()`, `np.log()`, etc.

**Example Workflow**:
```
1. Upload: temperature_experiment.csv
2. Select X: time, Y: temperature
3. Plot name: "temp_vs_time"
4. Equation: "Linear with intercept"
5. Click "Normal Fitting"
6. View results: y = 2.5·time + 20.3, R² = 0.98
7. Download plot
```

### Mode 2: Multiple Datasets

**Purpose**: Apply the same equation to multiple different files

**Steps**:

1. **Select Mode**:
   - In sidebar, click "Multiple Datasets"

2. **Select Equation First**:
   - Choose the equation type you'll use for all datasets
   - If using custom formula, define it here

3. **Upload Multiple Files**:
   - Click "Browse files"
   - **Hold Ctrl (Windows/Linux) or Cmd (Mac)** to select multiple files
   - Or use drag-and-drop for multiple files
   - All files upload simultaneously

4. **Configure Each Dataset**:
   - For each uploaded file:
     - File name shown as heading
     - Select X variable
     - Select Y variable
     - Enter plot name (defaults to filename)

5. **Fit All Datasets**:
   - Click the "Multiple Datasets" button (centered, blue)
   - All datasets are fitted sequentially
   - Progress indicators shown

6. **Review All Results**:
   - Results displayed for each dataset
   - Each has its own:
     - Equation
     - Parameters
     - Plot
     - Download button
   - Scroll through results to compare

**Tips**:
- All files should have similar column names
- X and Y variables can be different for each file if needed
- Results appear in upload order

**Example Workflow**:
```
1. Equation: "Quadratic"
2. Upload 3 files:
   - sample1.csv
   - sample2.csv
   - sample3.csv
3. For each:
   - X: concentration
   - Y: absorbance
4. Click "Multiple Datasets"
5. Review 3 separate fit results
6. Compare parameters and R² values
```

### Mode 3: Checker Fitting

**Purpose**: Test multiple equations on the same dataset to find the best fit

**Steps**:

1. **Select Mode**:
   - In sidebar, click "Checker Fitting"

2. **Upload Data**:
   - Upload your single data file

3. **Select Variables**:
   - Choose X and Y variables
   - Enter plot name

4. **Select Multiple Equations**:
   - Click in the "Select equation" dropdown
   - **Select multiple options** by clicking each one
   - Options remain in the dropdown (multi-select)
   - Default: First 3 equations pre-selected
   - Custom formulas not available in this mode

5. **Run Checker Fitting**:
   - Click "Checker Fitting" button
   - Progress bar shows completion
   - Each equation fitted sequentially

6. **Compare Results**:
   - All results displayed vertically
   - Compare:
     - R² values (higher is better)
     - Visual fit quality in plots
     - Parameter values
   - Identify the best-fitting equation

**Example Workflow**:
```
1. Upload: unknown_relationship.xlsx
2. X: voltage, Y: current
3. Select equations:
   - Linear with intercept (y=mx+n)
   - Quadratic (y=ax²)
   - Inverse (y=a/x)
   - Logarithmic (y=a·ln(x))
4. Click "Checker Fitting"
5. Compare results:
   - Linear: R²=0.75 (poor)
   - Quadratic: R²=0.92 (good)
   - Inverse: R²=0.98 (excellent!) ← Best fit
   - Logarithmic: R²=0.85 (acceptable)
6. Conclusion: Use inverse function
```

### Mode 4: Total Fitting

**Purpose**: Automatically test ALL available equations on your dataset

**Steps**:

1. **Select Mode**:
   - In sidebar, click "Total Fitting"

2. **Upload Data**:
   - Upload your data file

3. **Select Variables**:
   - Choose X and Y variables
   - Enter plot name

4. **Run Total Fitting**:
   - Info message shows: "Total Fitting: [N] equations"
   - Click "Total Fitting" button
   - Progress bar shows completion
   - **All** predefined equations fitted automatically
   - Takes longer than other modes

5. **Review All Results**:
   - Comprehensive results for all equation types
   - Scroll through to find the best fit
   - Look for highest R² value

**Use Cases**:
- Exploratory data analysis
- No prior knowledge of expected relationship
- Creating comprehensive reports
- Educational purposes (see all function types)

**Example Workflow**:
```
1. Upload: mystery_data.csv
2. X: x, Y: y
3. Plot name: "comprehensive_analysis"
4. Click "Total Fitting"
5. Wait for all 13+ equations to fit
6. Scan through results:
   - Linear: R²=0.60
   - Quadratic: R²=0.65
   - Sin with phase: R²=0.99 ← Best!
   - Logarithmic: R²=0.45
   - ... etc.
7. Use "Sin with phase" for this data
```

## Data Upload

### Supported Formats

- **CSV** (`.csv`): Comma-separated values
- **Excel** (`.xlsx`): Microsoft Excel files
- **TXT** (`.txt`): Tab-separated or space-separated text files

### File Size Limits

- **Online version**: Limited by Streamlit Cloud (typically 200 MB)
- **Local version**: Limited by your computer's memory

### Upload Methods

1. **Click "Browse files"**: Opens file picker dialog
2. **Drag and drop**: Drag files from your file manager into the upload area

### Multiple File Upload

- Hold **Ctrl** (Windows/Linux) or **Cmd** (Mac) while selecting
- Or drag multiple files at once
- Only available in "Multiple Datasets" mode

### Data Preview

After upload, expand "Show Data" to see:
- First and last rows
- All columns
- Data types
- Verify data loaded correctly

## Understanding Results

### Equation Display

The fitted equation is shown in mathematical notation:

```
y = 5.123·x + 2.456
```

- Parameters replaced with fitted values
- Uses standard mathematical symbols (·, ², etc.)

### Parameter Display

Parameters shown with uncertainties:

```
Parameter Results:
m = 5.123 ± 0.045
n = 2.456 ± 0.123
```

- Each parameter on its own line
- ± indicates uncertainty (standard error)

### Plot Components

**Data Points**:
- Red circles (or other markers)
- Error bars if uncertainties provided
- Your original measurements

**Fitted Curve**:
- Black line (or configured color)
- Smooth curve through data
- Based on fitted equation

**Axis Labels**:
- X-axis: Your X variable name
- Y-axis: Your Y variable name

**Legend** (if shown):
- Equation with parameters
- R² value

### R² Value (Coefficient of Determination)

**Interpretation**:
- **R² = 1.0**: Perfect fit (rare in real data)
- **R² > 0.95**: Excellent fit ✓
- **R² > 0.85**: Good fit ✓
- **R² > 0.70**: Acceptable fit ⚠️
- **R² < 0.70**: Poor fit - try different equation ✗

**What it means**:
- Percentage of variance explained by the model
- R² = 0.95 means 95% of variance explained
- Higher is better

### Downloading Plots

1. Scroll to the result you want
2. Click "📥 Download" button
3. Plot saved as PNG image
4. Default filename: `[plot_name].png`

**Download Tips**:
- Download all plots you need before closing browser
- Plots are high-resolution (configured DPI)
- PNG format preserves quality

## Tips and Best Practices

### Performance Tips

1. **Use local version for large datasets**: Faster than online
2. **Close unused browser tabs**: Frees memory
3. **One mode at a time**: Don't switch modes mid-analysis
4. **Clear results**: Refresh page to clear old results and free memory

### Data Tips

1. **Check data preview**: Always expand "Show Data" to verify upload
2. **Name columns clearly**: Use descriptive names like "time_s", "voltage_V"
3. **Remove headers in Excel**: Only column names in first row, data starts row 2
4. **Consistent units**: Ensure all data uses the same units

### Workflow Tips

1. **Start with Normal Fitting**: Test single equation first
2. **Use Checker for exploration**: When uncertain about best equation
3. **Use Total for comprehensive analysis**: When time permits
4. **Document your results**: Download all relevant plots

### Uncertainty Handling

If your data has uncertainties:
- Name columns `ux`, `uy` (lowercase 'u' + variable name)
- Example: for variable `time`, uncertainty column is `utime`
- Error bars appear automatically in plots
- Fitting is weighted by uncertainties

### Custom Formula Tips

1. **Test simple formulas first**: Try `a*x` before complex expressions
2. **Use parentheses**: `a/(1+b*x)` not `a/1+b*x`
3. **Available functions**: `np.sin()`, `np.cos()`, `np.exp()`, `np.log()`, `np.sqrt()`
4. **Check parameter count**: Must match number of parameters defined

## Troubleshooting

### Upload Issues

**Problem**: File won't upload

**Solutions**:
- Check file format (CSV, XLSX, TXT only)
- Try smaller file
- Check internet connection (online version)
- Refresh page and try again

### Fitting Fails

**Problem**: "Fitting error" message appears

**Possible causes**:
- Not enough data points (need at least 5-10)
- Data doesn't match equation type
- Infinite or NaN values in data
- All Y values are the same

**Solutions**:
- Check data for errors
- Try different equation type
- Ensure sufficient data points
- Remove outliers or bad data

### Results Not Showing

**Problem**: Clicked fit button but no results appear

**Solutions**:
- Wait for processing (check for spinner)
- Scroll down (results may be below viewport)
- Check browser console for errors (F12)
- Refresh page and try again

### App is Slow

**Problem**: App responds slowly or freezes

**Solutions**:
- Use local version instead of online
- Reduce dataset size
- Close other browser tabs
- Clear browser cache
- Refresh the app

### Download Doesn't Work

**Problem**: Can't download plots

**Solutions**:
- Check browser's download settings
- Allow downloads from streamlit.app domain
- Try right-click → "Save image as"
- Use different browser

## Keyboard Shortcuts

While Streamlit doesn't have extensive keyboard shortcuts, these work:

- **Ctrl+R / Cmd+R**: Refresh the app
- **F5**: Refresh the page
- **F11**: Full screen mode
- **Ctrl+Plus / Cmd+Plus**: Zoom in
- **Ctrl+Minus / Cmd+Minus**: Zoom out

## Mobile and Tablet Usage

The Streamlit interface is responsive and works on mobile devices:

**Recommendations**:
- Use landscape orientation for better plot viewing
- Tap and pinch to zoom plots
- Use tablet or larger for easier interaction
- Desktop recommended for serious work

## Advanced Features

### Session Persistence

- Results persist during your browser session
- Refresh clears all results
- Online version: sessions timeout after inactivity

### Multiple Tabs

You can open multiple browser tabs with RegressionLab:
- Each tab is independent
- Useful for comparing different analyses
- Be mindful of memory usage

## Differences from Tkinter Version

**Streamlit has**:
- ✓ Modern, web-based interface
- ✓ Easy sharing via URL
- ✓ Mobile/tablet support
- ✓ No installation needed (online)

**Streamlit lacks**:
- ✗ Loop mode for iterative fitting
- ✗ Advanced customization options
- ✗ Some keyboard shortcuts
- ✗ Local file browsing (must upload)

**When to use each**:
- **Streamlit**: Quick analysis, sharing, accessibility
- **Tkinter**: Advanced features, offline, customization

## Next Steps

- **Learn Tkinter**: See [Tkinter Guide](tkinter-guide) for desktop version
- **Customize**: Configure appearance in [Configuration Guide](configuration)
- **Extend**: Learn to add functions in [Extending RegressionLab](extending)

---

*Happy fitting! If you encounter issues, check the [Troubleshooting Guide](troubleshooting).*
