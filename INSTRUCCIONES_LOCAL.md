# BATALLA NAVAL - CONFIGURACIÓN LOCAL

## Instrucciones para jugar en localhost (dos jugadores en la misma PC)

### MÉTODO RÁPIDO (Recomendado)
1. **Ejecuta `iniciar_todo_local.bat`**
   - Este archivo limpia procesos anteriores automáticamente
   - Inicia servidor + ambos clientes automáticamente
   - Se abrirán 3 ventanas: Servidor, Jugador 1, y Jugador 2
   - Los clientes ya están configurados para conectarse automáticamente

### MÉTODO MANUAL (Paso a paso)

#### Paso 1: Iniciar el servidor
1. **OPCIÓN A (Recomendado)**: Ejecuta `run_server_clean.bat`
   - Limpia automáticamente procesos anteriores
   - Inicia el servidor limpio
2. **OPCIÓN B**: Ejecuta `run_server_local.bat` o directamente `python server.py`
3. El servidor se iniciará en `localhost:8889`
4. Verás el mensaje: "✅ Servidor iniciado en 0.0.0.0:8889"

#### Paso 2: Conectar el primer jugador
1. Ejecuta `run_client.bat` o directamente `python main.py`
2. En el menú, selecciona "Multijugador Online"
3. La dirección ya viene configurada por defecto como `127.0.0.1:8889`
4. Presiona "Conectar"

#### Paso 3: Conectar el segundo jugador
1. Ejecuta `run_client_player2.bat` o abre otra terminal y ejecuta `python main.py`
2. Repite el proceso de conexión
3. Una vez conectados ambos jugadores, pueden iniciar la partida

### Archivos disponibles:
- **`iniciar_todo_local.bat`** - Inicia servidor + 2 clientes automáticamente con limpieza (RECOMENDADO)
- **`run_server_clean.bat`** - Servidor con limpieza automática (RECOMENDADO)
- **`run_server_local.bat`** - Solo servidor (sin limpieza)
- **`run_client.bat`** - Cliente Jugador 1
- **`run_client_player2.bat`** - Cliente Jugador 2
- **`server.py`** - Servidor del juego (manual)
- **`main.py`** - Cliente del juego (manual)

### Configuración por defecto:
- **Host**: 127.0.0.1 (localhost)
- **Puerto**: 8889
- **Máximo jugadores**: 2

### Notas importantes:
- El servidor debe estar ejecutándose antes de que los clientes se conecten
- Ambos clientes pueden ejecutarse desde la misma PC
- Cada jugador tendrá su propia ventana del juego
- Para detener el servidor, presiona Ctrl+C en la ventana del servidor
- Si cambias la configuración del servidor, asegúrate de actualizar también la dirección en los clientes

### Solución de problemas:
1. **Error "Connection refused"**: Asegúrate de que el servidor esté ejecutándose
2. **Error "Puerto ocupado" (WinError 10048)**: 
   - Usa `run_server_clean.bat` en lugar de `run_server_local.bat`
   - O ejecuta manualmente: `taskkill /F /IM python.exe` y luego `python server.py`
3. **Servidor lleno**: Solo se permiten 2 jugadores máximo
4. **Problemas de conexión**: Verifica que estés usando la dirección correcta (127.0.0.1:8889)
5. **Puerto ocupado**: Si el puerto 8889 está ocupado, puedes cambiar el puerto en `server.py` y `network.py`

### Cómo jugar:
1. Una vez conectados ambos jugadores, cualquiera puede presionar "Iniciar Juego"
2. Ambos jugadores colocarán sus barcos en sus respectivos tableros
3. Una vez colocados todos los barcos, comenzará la batalla
4. Los jugadores se turnan para disparar al tablero enemigo
5. El primer jugador en hundir todos los barcos enemigos gana