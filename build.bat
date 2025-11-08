@echo off
setlocal

REM Simple build script for AeroVolt HomeFlow G-Assist plugin

echo [AeroVolt HomeFlow] Creating virtual environment (if not exists)...
if not exist venv (
    python -m venv venv
)

call venv\Scripts\activate

echo [AeroVolt HomeFlow] Installing requirements...
pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller

echo [AeroVolt HomeFlow] Building g-assist-plugin-homeflow.exe ...
pyinstaller ^
  --onefile ^
  --name g-assist-plugin-homeflow ^
  plugin.py

echo [AeroVolt HomeFlow] Build finished. EXE should be in the dist folder.
echo [AeroVolt HomeFlow] Copy dist\g-assist-plugin-homeflow.exe into your G-Assist plugins\homeflow folder.

endlocal
