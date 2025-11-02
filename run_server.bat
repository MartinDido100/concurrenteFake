@echo off
:: Script para iniciar el servidor en modo online con ngrok
title Batalla Naval - Servidor Online (ngrok)

echo.
echo ========================================================================
echo                BATALLA NAVAL - SERVIDOR ONLINE (ngrok)
echo ========================================================================
echo.
echo Este script iniciara el servidor con soporte para ngrok
echo Los jugadores podran conectarse desde cualquier parte del mundo
echo.
echo IMPORTANTE:
echo - Necesitas tener ngrok instalado
echo - Se te proporcionara una URL publica para compartir con los jugadores
echo - Mantén esta ventana abierta mientras juegas
echo.
echo ========================================================================
echo.

pause

:: Ejecutar el script de Python para servidor online
python start_server_online.py

pause
