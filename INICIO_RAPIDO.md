# 🚢 Batalla Naval - Inicio Rápido

## 🎮 Modo de Juego

### 🏠 Jugar en LAN (Misma Red WiFi)

**Servidor:**
```bash
# Doble click en:
run_server.bat
```

**Clientes:**
```bash
# Doble click en:
run_client.bat

# En el juego:
1. Click "Conectar a Servidor"
2. Seleccionar "LAN (Local)"
3. Host: localhost (para servidor) o IP local (para otros)
4. Puerto: 8888
```

---

### 🌐 Jugar Online (Internet con ngrok)

#### 📋 Requisitos Previos:
1. Instalar ngrok: https://ngrok.com/download
2. Colocar `ngrok.exe` en la carpeta del juego

#### 🖥️ Servidor (1 jugador):

```bash
# Doble click en:
run_server_online.bat

# Copiar la URL que aparece:
# Ejemplo: tcp://0.tcp.ngrok.io:12345
#   Host: 0.tcp.ngrok.io
#   Puerto: 12345
```

**Compartir** Host y Puerto con el otro jugador

#### 🎮 Cliente en Servidor (Jugador 1):

```bash
# Doble click en:
run_client.bat

# En el juego:
1. Click "Conectar a Servidor"
2. Seleccionar "LAN (Local)"
3. Host: localhost
4. Puerto: 8888
```

#### 🎮 Cliente Remoto (Jugador 2):

```bash
# Doble click en:
run_client.bat

# En el juego:
1. Click "Conectar a Servidor"
2. Seleccionar "Online (ngrok)"
3. Host: [URL recibida del servidor]
4. Puerto: [Puerto recibido del servidor]
```

---

## 🔧 Instalación Rápida

### Opción 1: Script Automático (Recomendado)
```bash
# Doble click en:
install_and_run.ps1
# O
install_and_run.bat

# Instala todo automáticamente y ejecuta el juego
```

### Opción 2: Manual
```bash
# Verificar Python
python --version

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar
python main.py
```

---

## 📖 Documentación Completa

- **Guía de Juego Online**: Ver `GUIA_JUEGO_ONLINE.md`
- **Instalador Automático**: Ver `INSTALADOR_README.md`

---

## ⚡ Solución Rápida de Problemas

**"No se encuentra ngrok"**
→ Descargar de https://ngrok.com/download y colocar en carpeta del juego

**"No se puede conectar"**
→ Verificar que el servidor esté ejecutándose primero

**"pygame no está instalado"**
→ Ejecutar: `pip install pygame`

---

## 🎯 Flujo Simple

```
Servidor:  run_server_online.bat → Copiar URL → Compartir
Cliente 1: run_client.bat → LAN → localhost:8888
Cliente 2: run_client.bat → Online → [URL de ngrok]
→ ¡A jugar!
```

---

¡Disfruta del juego! ⚓🚢
