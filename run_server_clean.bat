@echo off
title BATALLA NAVAL - LIMPIEZA Y SERVIDOR
cls
echo =====================================
echo    BATALLA NAVAL - SERVIDOR LIMPIO
echo =====================================
echo.
echo Limpiando procesos anteriores...

REM Terminar cualquier proceso Python que pueda estar usando el puerto
echo Terminando procesos Python anteriores...
taskkill /F /IM python.exe >nul 2>&1

REM Esperar un momento para que se liberen los puertos
timeout /t 2 /nobreak > nul

echo ✅ Procesos limpiados
echo.
echo Iniciando servidor en localhost:8889
echo.
echo Para jugar:
echo 1. Ejecuta este archivo para iniciar el servidor
echo 2. Ejecuta main.py dos veces (una por cada jugador)
echo 3. En ambos clientes, conecta a 127.0.0.1:8889
echo.
echo Presiona Ctrl+C para detener el servidor
echo =====================================
echo.

python server.py

pause