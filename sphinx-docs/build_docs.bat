@echo off
REM Build RegressionLab Documentation

echo Building RegressionLab documentation...
echo.

REM Clean previous build
call make.bat clean

REM Build HTML documentation
call make.bat html

echo.
echo Documentation build complete!
echo.
echo Open build\html\index.html in your browser to view the documentation.
echo.

pause
