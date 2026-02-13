@echo off
chcp 65001 >nul
cd /d "%~dp0"

if not exist "env\Scripts\python.exe" (
    echo Ambiente virtual nao encontrado!
    pause
    exit /b
)

env\Scripts\python.exe -m scripts.menu_relatorios
pause
