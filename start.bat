@echo off
cd /d "%~dp0"
if exist "%~dp0launch_silent.vbs" (
  wscript //nologo "%~dp0launch_silent.vbs"
  exit /b 0
)
set "PYW=%LocalAppData%\Python\pythoncore-3.14-64\pythonw.exe"
if not exist "%PYW%" set "PYW=%LocalAppData%\Python\bin\pythonw.exe"
if not exist "%PYW%" set "PYW=pythonw"
start "" /D "%~dp0" "%PYW%" "%~dp0main.py"
exit /b 0
