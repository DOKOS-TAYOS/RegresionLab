@echo off
REM Open RegressionLab Documentation in Browser
REM Uses script directory so it works from any CWD.

set "DOCINDEX=%~dp0build\html\index.html"

echo Opening RegressionLab documentation...
if exist "%DOCINDEX%" (
    start "" "%DOCINDEX%"
) else (
    echo ERROR: Documentation not found.
    echo Looked at: %DOCINDEX%
    echo.
    echo Build the docs from this folder first: sphinx-docs\build_docs.bat
    pause
    exit /b 1
)
