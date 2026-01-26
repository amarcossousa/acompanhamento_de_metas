@echo off
chcp 65001 > nul
setlocal EnableDelayedExpansion

REM ===============================
REM  GERADOR DE RELATORIOS
REM ===============================

REM Caminho da venv (ajuste se necessário)
if not exist "env\Scripts\activate.bat" (
    echo ERRO: Ambiente virtual nao encontrado.
    echo Verifique se a pasta "env" existe.
    pause
    exit /b
)

call env\Scripts\activate.bat

:MENU
cls
echo ===============================
echo  GERADOR DE RELATORIOS
echo ===============================
echo.

set MES=
set ANO=

set /p MES=Informe o mes (1 a 12): 
set /p ANO=Informe o ano (ex: 2026): 

echo.
echo Gerando relatorio para %MES%/%ANO%
echo.

python run_relatorio.py %MES% %ANO%

echo.
echo ===============================
set CONT=
set /p CONT=Deseja gerar outro relatorio? (S/N): 

if /I "%CONT%"=="S" goto MENU

echo.
echo Encerrando o programa
pause
