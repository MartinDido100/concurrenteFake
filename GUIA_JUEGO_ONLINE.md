# 🌐 Batalla Naval - Guía de Juego Online con ngrok

Esta guía te explica cómo jugar Batalla Naval con amigos desde cualquier parte del mundo usando **ngrok**.

## 📋 Tabla de Contenidos

1. [¿Qué es ngrok?](#qué-es-ngrok)
2. [Instalación de ngrok](#instalación-de-ngrok)
3. [Configuración del Servidor](#configuración-del-servidor)
4. [Configuración del Cliente](#configuración-del-cliente)
5. [Jugar en LAN vs Online](#jugar-en-lan-vs-online)
6. [Solución de Problemas](#solución-de-problemas)

---

## 🤔 ¿Qué es ngrok?

**ngrok** es una herramienta que crea un túnel seguro desde Internet hacia tu computadora. Esto permite que otras personas se conecten a tu servidor de juego sin necesidad de configurar tu router ni conocer tu IP pública.

### Ventajas:
- ✅ **Fácil de usar**: No requiere configuración del router
- ✅ **Seguro**: Túnel encriptado
- ✅ **Gratis**: Plan gratuito disponible
- ✅ **Rápido**: Configuración en minutos

### Desventajas:
- ⚠️ **URL temporal**: La URL cambia cada vez que reinicias ngrok
- ⚠️ **Límites gratuitos**: Plan gratuito tiene limitaciones
- ⚠️ **Latencia adicional**: Pequeño retraso por el túnel

---

## 📥 Instalación de ngrok

### Opción 1: Instalación Manual (Recomendada)

1. **Descargar ngrok**
   - Ve a: https://ngrok.com/download
   - Descarga la versión para Windows
   - Extrae el archivo `ngrok.exe`

2. **Colocar ngrok.exe**
   
   **Opción A - En la carpeta del juego:**
   ```
   TP-Integrador/
   ├── ngrok.exe          <-- Coloca el archivo aquí
   ├── server.py
   ├── main.py
   └── ...
   ```
   
   **Opción B - En el PATH de Windows:**
   - Crea una carpeta: `C:\ngrok\`
   - Copia `ngrok.exe` ahí
   - Agregar al PATH:
     1. Busca "Variables de entorno" en Windows
     2. Edita la variable "Path"
     3. Agrega `C:\ngrok\`
     4. Reinicia CMD/PowerShell

3. **Autenticación (Opcional pero Recomendado)**
   ```bash
   # Crea cuenta gratuita en: https://dashboard.ngrok.com/signup
   # Copia tu token de autenticación
   # Ejecuta en CMD:
   ngrok authtoken TU_TOKEN_AQUÍ
   ```

### Opción 2: Instalación con Chocolatey (Avanzado)

```powershell
# Si tienes Chocolatey instalado:
choco install ngrok
```

### Opción 3: Instalación con Scoop (Avanzado)

```powershell
# Si tienes Scoop instalado:
scoop install ngrok
```

### Verificar Instalación

```bash
# En CMD o PowerShell:
ngrok version

# Deberías ver algo como:
# ngrok version 3.x.x
```

---

## 🖥️ Configuración del Servidor

### Método 1: Usando el Script Automático (Recomendado)

1. **Doble clic en `run_server_online.bat`**
   - El script verificará si ngrok está instalado
   - Si no está instalado, te dará instrucciones
   - Si está instalado, iniciará automáticamente el servidor y ngrok

2. **Copiar la información de conexión**
   ```
   ================================================================================
   ✅ TÚNEL NGROK ACTIVO
   ================================================================================
   🌐 URL pública de ngrok: tcp://0.tcp.ngrok.io:12345
   ================================================================================
   📋 Los jugadores deben usar esta información para conectarse:
      Host: 0.tcp.ngrok.io
      Puerto: 12345
   ================================================================================
   ```

3. **Compartir con los jugadores**
   - Envía el **Host** y **Puerto** por WhatsApp, Discord, etc.
   - Los jugadores usarán estos datos en el cliente

### Método 2: Manual (Avanzado)

**Terminal 1 - Iniciar Servidor:**
```bash
python server.py
```

**Terminal 2 - Iniciar ngrok:**
```bash
ngrok tcp 8888
```

Copia la URL de ngrok que aparece y compártela con los jugadores.

---

## 🎮 Configuración del Cliente

### Para el Jugador que Inicia el Servidor (Host)

1. Ejecuta `run_client.bat` o `python main.py`
2. Click en **"Conectar a Servidor"**
3. Selecciona **"LAN (Local)"**
4. Deja los valores por defecto:
   - Host: `localhost`
   - Puerto: `8888`
5. Click en **"Conectar"**

### Para Jugadores Remotos (Online)

1. Ejecuta `run_client.bat` o `python main.py`
2. Click en **"Conectar a Servidor"**
3. Selecciona **"Online (ngrok)"**
4. Ingresa la información que te compartió el host:
   - **Host**: `0.tcp.ngrok.io` (ejemplo)
   - **Puerto**: `12345` (ejemplo)
5. Click en **"Conectar"**

### Pantalla de Configuración de Conexión

```
┌─────────────────────────────────────────────────┐
│      Configuración de Conexión                  │
├─────────────────────────────────────────────────┤
│  Selecciona el modo de conexión:                │
│                                                  │
│  ┌──────────────┐  ┌──────────────┐            │
│  │ LAN (Local)  │  │Online(ngrok) │            │
│  └──────────────┘  └──────────────┘            │
│                                                  │
│  Host/IP: [____________________]                │
│  Puerto:  [____________________]                │
│                                                  │
│  ┌─────────┐  ┌─────────┐                      │
│  │Conectar │  │Cancelar │                      │
│  └─────────┘  └─────────┘                      │
└─────────────────────────────────────────────────┘
```

---

## 🎯 Jugar en LAN vs Online

### 🏠 Modo LAN (Red Local)

**Cuándo usar:**
- Ambos jugadores en la misma casa/oficina
- Conectados a la misma WiFi
- Quieres menor latencia

**Configuración:**
- **Servidor**: Ejecuta `run_server.bat`
- **Cliente 1** (en servidor): Host = `localhost`, Puerto = `8888`
- **Cliente 2** (otra PC): Host = `IP_LOCAL_SERVIDOR`, Puerto = `8888`

**Obtener IP Local:**
```bash
# En CMD del servidor:
ipconfig

# Buscar "IPv4" - algo como: 192.168.1.100
```

### 🌐 Modo Online (Internet)

**Cuándo usar:**
- Jugadores en casas diferentes
- Jugadores en ciudades/países diferentes
- No tienes acceso al router

**Configuración:**
- **Servidor**: Ejecuta `run_server_online.bat`
- **Cliente 1** (en servidor): Host = `localhost`, Puerto = `8888`
- **Cliente 2** (remoto): Host = `URL_NGROK`, Puerto = `PUERTO_NGROK`

---

## 🔧 Solución de Problemas

### ❌ "ngrok no está instalado"

**Solución:**
1. Descarga ngrok desde: https://ngrok.com/download
2. Coloca `ngrok.exe` en la carpeta del juego
3. O agrégalo al PATH de Windows
4. Verifica con: `ngrok version`

### ❌ "Error al obtener URL de ngrok"

**Causas posibles:**
- ngrok no terminó de iniciar (espera 10 segundos)
- Firewall bloqueando ngrok
- Puerto 4040 (API de ngrok) ocupado

**Soluciones:**
1. Cierra otros procesos de ngrok: `taskkill /F /IM ngrok.exe`
2. Reinicia el script
3. Verifica firewall de Windows

### ❌ "No se pudo conectar al servidor"

**Para modo LAN:**
1. Verifica que el servidor esté ejecutándose
2. Verifica la IP local: `ipconfig`
3. Desactiva temporalmente el firewall para probar
4. Asegúrate de estar en la misma red WiFi

**Para modo Online:**
1. Verifica que ngrok esté ejecutándose
2. Copia exactamente la URL de ngrok (sin espacios)
3. Verifica el puerto
4. Reinicia ngrok si la URL expiró

### ❌ "Túnel ngrok cerrado"

**Causas:**
- Plan gratuito tiene límite de tiempo
- Reiniciaste ngrok
- Problemas de conexión

**Solución:**
1. Reinicia `run_server_online.bat`
2. Comparte la **nueva URL** con los jugadores
3. Reconecta desde los clientes

### ❌ Lag o alta latencia

**Para modo Online:**
- Es normal tener algo de latencia con ngrok
- Prueba el plan de pago de ngrok para mejor rendimiento
- O cambia a modo LAN si es posible

**Optimizaciones:**
1. Cierra otras aplicaciones que usen Internet
2. Usa conexión por cable en vez de WiFi
3. Verifica que no haya descargas activas

### ❌ "Error: rate limit exceeded"

**Causa:**
- Plan gratuito de ngrok tiene límites de conexiones

**Soluciones:**
1. Autentícate con cuenta ngrok: `ngrok authtoken TU_TOKEN`
2. Espera unos minutos y reinicia
3. Considera plan de pago de ngrok

---

## 📊 Comparación de Modos

| Característica | LAN | Online (ngrok) |
|----------------|-----|----------------|
| **Configuración** | Fácil | Media |
| **Latencia** | Muy baja (~1ms) | Baja-Media (50-200ms) |
| **Alcance** | Red local | Mundial |
| **Router** | No requiere cambios | No requiere cambios |
| **Costo** | Gratis | Gratis (con límites) |
| **Estabilidad** | Muy alta | Alta |
| **URL** | IP fija local | URL temporal |

---

## 🎮 Flujo Completo de Juego Online

### 🖥️ Jugador 1 (Servidor/Host)

1. ✅ Instalar ngrok
2. ✅ Ejecutar `run_server_online.bat`
3. ✅ Copiar URL y Puerto de ngrok
4. ✅ Compartir con Jugador 2
5. ✅ Ejecutar `run_client.bat`
6. ✅ Conectar con modo "LAN" → localhost:8888
7. ✅ Esperar al Jugador 2
8. ✅ Iniciar partida

### 🎮 Jugador 2 (Cliente Remoto)

1. ✅ Recibir URL y Puerto del Jugador 1
2. ✅ Ejecutar `run_client.bat`
3. ✅ Conectar con modo "Online"
4. ✅ Ingresar Host y Puerto recibidos
5. ✅ Esperar a que Jugador 1 inicie
6. ✅ ¡A jugar!

---

## 📞 Soporte y Ayuda

### Recursos Útiles

- **ngrok Docs**: https://ngrok.com/docs
- **ngrok Dashboard**: https://dashboard.ngrok.com/
- **ngrok Download**: https://ngrok.com/download

### Tips Adicionales

1. **Autenticación mejora el servicio**:
   ```bash
   ngrok authtoken TU_TOKEN
   ```

2. **Ver conexiones activas**:
   - Abre: http://localhost:4040 (mientras ngrok está activo)

3. **Usar región específica** (menos latencia):
   ```bash
   ngrok tcp 8888 --region sa  # Sudamérica
   ngrok tcp 8888 --region us  # USA
   ngrok tcp 8888 --region eu  # Europa
   ```

4. **Mantén las ventanas abiertas**:
   - Servidor debe estar ejecutándose
   - ngrok debe estar ejecutándose
   - No cierres las ventanas durante el juego

---

## 🏆 ¡Listo para Jugar!

Ahora puedes disfrutar de Batalla Naval con amigos desde cualquier parte del mundo. 

¡Buena suerte, marinero! ⚓🚢

---

**Fecha de actualización**: Noviembre 2025  
**Versión**: 1.0
