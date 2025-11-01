@echo off
title Batalla Naval - Servidor LAN
echo.
echo ========================================================================
echo                BATALLA NAVAL - SERVIDOR LAN (Red Local)
echo ========================================================================
echo.
echo Este servidor permite conexiones en la red local (LAN)
echo Los jugadores deben estar en la misma red WiFi/Ethernet
echo.
echo Para jugar por Internet, usa: run_server_online.bat
echo.
echo ========================================================================
echo.
echo Iniciando servidor de Batalla Naval...
echo Presiona Ctrl+C para detener el servidor
echo.
python server.py
pause