@echo off
REM ============================================================================
REM RegressionLab - Installation Script for Windows
REM ============================================================================
REM This script clones the repository and runs the setup automatically
REM ============================================================================

echo.
echo ====================================
echo    RegressionLab Installation
echo ====================================
echo.

REM Check if Git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git is not installed or not in PATH
    echo Please install Git from https://git-scm.com/download/win
    echo.
    pause
    exit /b 1
)

echo [1/3] Git found: 
git --version

REM Set repository URL
set "REPO_URL=https://github.com/DOKOS-TAYOS/RegressionLab.git"
set "REPO_NAME=regressionlab"

REM Check if directory already exists
if exist "%REPO_NAME%" (
    echo.
    echo WARNING: Directory '%REPO_NAME%' already exists
    set /p OVERWRITE="Do you want to remove it and clone again? (y/N): "
    if /i "%OVERWRITE%"=="y" (
        echo       Removing existing directory...
        rmdir /s /q "%REPO_NAME%" 2>nul
    ) else (
        echo       Using existing directory...
        cd "%REPO_NAME%"
        goto :run_setup
    )
)

echo.
echo [2/3] Cloning repository...
git clone "%REPO_URL%"
if errorlevel 1 (
    echo ERROR: Failed to clone repository
    echo Please check your internet connection and try again
    pause
    exit /b 1
)

echo       Repository cloned successfully

REM Change to repository directory
cd "%REPO_NAME%"
if errorlevel 1 (
    echo ERROR: Failed to change to repository directory
    pause
    exit /b 1
)

:run_setup
echo.
echo [3/3] Running setup...
echo.
call setup.bat
if errorlevel 1 (
    echo.
    echo ERROR: Setup failed
    pause
    exit /b 1
)

echo.
echo ====================================
echo    Installation Complete!
echo ====================================
echo.
echo The RegressionLab repository has been cloned and set up.
echo You can now run the application from: %CD%
echo.
pause
