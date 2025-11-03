@echo off
title BATALLA NAVAL - LIMPIEZA DE PUERTOS
cls
echo =====================================
echo   BATALLA NAVAL - LIMPIEZA PUERTOS
echo =====================================
echo.
echo Este script limpiará todos los procesos Python
echo que puedan estar ocupando el puerto 8889
echo.

echo Terminando procesos Python...
taskkill /F /IM python.exe >nul 2>&1

echo Esperando que se liberen los puertos...
timeout /t 3 /nobreak > nul

echo.
echo ✅ Limpieza completada
echo.
echo Verificando que el puerto 8889 esté libre...
netstat -ano | findstr :8889
if %ERRORLEVEL% == 0 (
    echo ❌ El puerto 8889 todavía está ocupado
    echo    Intenta reiniciar la computadora si persiste el problema
) else (
    echo ✅ Puerto 8889 está libre
    echo    Ya puedes iniciar el servidor
)

echo.
pause