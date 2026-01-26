@echo off
REM Ativa o ambiente virtual
call venv\Scripts\activate

REM Executa o script Python
python run_relatorio.py

REM Pausa para ver mensagens de erro ou sucesso
pause
