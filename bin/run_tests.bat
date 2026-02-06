@echo off
REM Run all tests for RegressionLab project

REM Change to project root directory (parent of bin)
cd /d "%~dp0.."

REM Activate virtual environment if it exists
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
)

echo Running RegressionLab tests...
python tests\run_tests.py
pause
