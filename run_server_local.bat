@echo off
title BATALLA NAVAL - SERVIDOR LOCAL
cls
echo =====================================
echo    BATALLA NAVAL - SERVIDOR LOCAL
echo =====================================
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