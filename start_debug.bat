@echo off
title Nexus Performante Arena (debug console)
cd /d "%~dp0"

set "PY=%LocalAppData%\Python\pythoncore-3.14-64\python.exe"
if not exist "%PY%" set "PY=%LocalAppData%\Python\bin\python.exe"
if not exist "%PY%" set "PY=python"

echo Using: %PY%
echo.
"%PY%" -c "import psutil, pystray, PIL; print('deps OK')" 2>&1
if errorlevel 1 (
  echo Installing requirements...
  "%PY%" -m pip install -r requirements.txt
)
echo.
echo Starting with console (errors will show here)...
echo.
"%PY%" "%~dp0main.py"
echo.
echo Exit code: %errorlevel%
if exist "%~dp0launch_error.log" (
  echo --- launch_error.log ---
  type "%~dp0launch_error.log"
)
pause
