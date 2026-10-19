@echo off
title Build Nexus Performante Arena EXE
cd /d "%~dp0"

set "PY=%LocalAppData%\Python\pythoncore-3.14-64\python.exe"
if not exist "%PY%" set "PY=%LocalAppData%\Python\bin\python.exe"
if not exist "%PY%" set "PY=python"

echo Using: %PY%
echo.

"%PY%" -m pip install pyinstaller pillow -q
"%PY%" -c "from PIL import Image; from pathlib import Path; im=Image.open('assets/logo.png').convert('RGBA'); w,h=im.size; s=min(w,h); im=im.crop(((w-s)//2,(h-s)//2,(w-s)//2+s,(h-s)//2+s)); im.save('assets/logo.ico', format='ICO', sizes=[(16,16),(32,32),(48,48),(64,64),(128,128),(256,256)]); print('logo.ico ready')"

echo Building EXE (this can take a minute)...
"%PY%" -m PyInstaller --noconfirm --clean --windowed --onefile ^
  --name "NexusPerformanteArena" ^
  --icon "assets\logo.ico" ^
  --add-data "assets;assets" ^
  --add-data "mp3player.py;." ^
  --hidden-import "PIL._tkinter_finder" ^
  --hidden-import "pystray._win32" ^
  --collect-all "yt_dlp" ^
  main.py

if errorlevel 1 (
  echo BUILD FAILED
  pause
  exit /b 1
)

copy /Y "dist\NexusPerformanteArena.exe" "%USERPROFILE%\Desktop\NexusPerformanteArena.exe" >nul
echo.
echo  Done!
echo  Folder: %cd%\dist\NexusPerformanteArena.exe
echo  Desktop: %USERPROFILE%\Desktop\NexusPerformanteArena.exe
echo.
pause
