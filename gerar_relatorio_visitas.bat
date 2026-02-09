@echo off
chcp 65001 >nul
title 📊 Gerador de Relatórios - Visitas API
color 0A

REM Garante que está na raiz do projeto
cd /d "%~dp0"

cls
echo ==========================================
echo  📊 GERADOR DE RELATÓRIOS - VISITAS API
echo ==========================================
echo.

REM Verifica se a venv existe
if not exist "venv\Scripts\python.exe" (
    echo ❌ Ambiente virtual não encontrado!
    echo 👉 Esperado em: venv\Scripts\python.exe
    echo.
    pause
    exit /b
)

:MENU
echo ------------------------------------------
echo 📅 Informe os dados do relatório
echo ------------------------------------------

set /p MES=📅 Mês (1 a 12) [padrão 1]: 
if "%MES%"=="" set MES=1

set /p ANO=📆 Ano [padrão 2026]: 
if "%ANO%"=="" set ANO=2026

echo.
echo ▶ Gerando relatório para %MES%/%ANO%
echo ⏳ Aguarde. Buscando dados do coletum API...
echo.

REM Executa usando o python da venv
venv\Scripts\python.exe -m scripts.run_relatorio_visitas_api %MES% %ANO%

echo.
echo ✅ Relatório finalizado!
echo 📂 Pasta: reports\
echo.

set /p NOVO=🔁 Deseja gerar outro relatório? (S/N): 
if /I "%NOVO%"=="S" (
    cls
    goto MENU
)

echo.
echo 👋 Encerrando o gerador de relatórios
pause
