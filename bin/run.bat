@echo off
REM ============================================================================
REM RegressionLab - Quick Launch Script for Windows
REM ============================================================================
REM This script activates the virtual environment and runs RegressionLab
REM ============================================================================

REM Language Configuration (Uncomment and modify to set language)
REM set LANGUAGE=es    REM For Spanish (default)
REM set LANGUAGE=en    REM For English

REM Change to project root directory (parent of bin)
cd /d "%~dp0.."

REM Check if virtual environment exists
if not exist .venv (
    echo ERROR: Virtual environment not found
    echo Please run setup.bat first
    pause
    exit /b 1
)

REM Activate virtual environment and run the program (start = console closes after launch)
call .venv\Scripts\activate.bat
start "" pythonw src\main_program.py
