@echo off
REM Streamlit launcher for RegressionLab (Windows)
REM This script starts the Streamlit web application

echo Starting RegressionLab Streamlit Application...
echo.

REM Activate virtual environment if it exists
if exist .venv\Scripts\activate.bat (
    echo Activating virtual environment...
    call .venv\Scripts\activate.bat
)

REM Run Streamlit application
streamlit run src\streamlit_app\app.py

pause
