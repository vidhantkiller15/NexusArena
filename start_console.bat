@echo off
REM Hidden launch (no CMD window). For visible errors use start_debug.bat
cd /d "%~dp0"
if exist "%~dp0launch_silent.vbs" (
  wscript //nologo "%~dp0launch_silent.vbs"
  exit /b 0
)
start "" /D "%~dp0" "%LocalAppData%\Python\pythoncore-3.14-64\pythonw.exe" "%~dp0main.py"
exit /b 0
