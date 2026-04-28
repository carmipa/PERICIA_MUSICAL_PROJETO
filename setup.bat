@echo off
echo [*] Iniciando configuracao do ambiente para Pericia Musical...
echo [*] Instalando dependencias do Python...
pip install -r requirements.txt
echo.
echo [!] IMPORTANTE: Este projeto utiliza o FFmpeg para conversao de audio.
echo [!] Se voce nao tiver o FFmpeg instalado, os scripts podem falhar.
echo [!] Link para download: https://ffmpeg.org/download.html
echo.
echo [OK] Dependencias instaladas com sucesso!
pause
