@echo off
setlocal
cd /d "%~dp0"

if exist "venv\Scripts\python.exe" (
    "venv\Scripts\python.exe" "vault_gui.py"
) else (
    python "vault_gui.py"
)
