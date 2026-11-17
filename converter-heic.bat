@echo off
rem Windows: dois cliques abrem a caixa para escolher as fotos HEIC. So chama o script da skill converter-heic.
cd /d "%~dp0"
if not exist .venv\Scripts\python.exe py .agents\configurar.py
.venv\Scripts\python.exe .agents\skills\converter-heic\scripts\heic_para_jpg.py
pause
