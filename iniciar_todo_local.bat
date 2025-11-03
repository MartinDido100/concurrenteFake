@echo off
title BATALLA NAVAL - LAUNCHER COMPLETO
cls
echo =====================================
echo   BATALLA NAVAL - LAUNCHER COMPLETO
echo =====================================
echo.
echo Limpiando procesos anteriores...

REM Terminar cualquier proceso Python anterior
taskkill /F /IM python.exe >nul 2>&1

REM Esperar para que se liberen los puertos
timeout /t 2 /nobreak > nul

echo ✅ Procesos limpiados
echo.
echo Este script iniciará automáticamente:
echo 1. El servidor local (puerto 8889)
echo 2. Dos clientes (Jugador 1 y Jugador 2)
echo.
echo Espera 3 segundos para que inicie el servidor...
echo =====================================
echo.

REM Iniciar servidor en ventana separada
start "SERVIDOR LOCAL" cmd /k "cd /d %~dp0 && run_server_clean.bat"

REM Esperar 3 segundos para que el servidor inicie
timeout /t 3 /nobreak > nul

REM Iniciar primer cliente
start "JUGADOR 1" cmd /k "cd /d %~dp0 && run_client.bat"

REM Esperar 2 segundos antes del segundo cliente
timeout /t 2 /nobreak > nul

REM Iniciar segundo cliente
start "JUGADOR 2" cmd /k "cd /d %~dp0 && run_client_player2.bat"

echo.
echo ✅ Todos los procesos iniciados:
echo    - Servidor Local
echo    - Cliente Jugador 1
echo    - Cliente Jugador 2
echo.
echo Ahora puedes jugar desde ambas ventanas!
echo.
pause