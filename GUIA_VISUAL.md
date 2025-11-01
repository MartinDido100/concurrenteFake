# 🎮 Batalla Naval - Guía Visual Rápida

## 📁 Archivos Principales

```
TP-Integrador/
│
├── 🎮 JUEGO
│   ├── main.py                    - Archivo principal del juego
│   ├── run_client.bat            - Ejecutar cliente (doble click)
│   ├── server.py                  - Servidor del juego
│   └── network.py                 - Gestión de red
│
├── 🖥️ SERVIDOR
│   ├── run_server.bat            - Servidor LAN (doble click)
│   └── run_server_online.bat     - Servidor Online/ngrok (doble click)
│   └── start_server_online.py    - Script servidor con ngrok
│
├── ⚙️ INSTALACIÓN
│   ├── install_and_run.ps1       - Instalador PowerShell
│   ├── install_and_run.bat       - Instalador Batch
│   └── requirements.txt           - Dependencias
│
├── 📖 DOCUMENTACIÓN
│   ├── INICIO_RAPIDO.md          - ⭐ EMPIEZA AQUÍ
│   ├── GUIA_JUEGO_ONLINE.md      - Guía completa ngrok
│   ├── INSTALADOR_README.md      - Ayuda instalación
│   └── config.ini                 - Configuración servidor
│
└── 📦 ASSETS
    ├── images/                    - Imágenes del juego
    └── sounds/                    - Sonidos del juego
```

---

## 🚀 Inicio Ultra-Rápido

### Instalación (Primera vez)
```
1. Doble click en: install_and_run.ps1
   → Instala Python, pygame y ejecuta el juego automáticamente
```

### Jugar en LAN (Misma WiFi)
```
┌─────────────────┐      ┌─────────────────┐
│  COMPUTADORA 1  │      │  COMPUTADORA 2  │
│    (Servidor)   │      │    (Cliente)    │
└─────────────────┘      └─────────────────┘
         │                        │
         │  1. run_server.bat     │  1. run_client.bat
         │  2. run_client.bat     │  2. Conectar → LAN
         │  3. Conectar → LAN     │  3. Host: [IP servidor]
         │  4. localhost:8888     │  4. Puerto: 8888
         │                        │
         └────────────────────────┘
              Misma WiFi
```

### Jugar Online (Internet)
```
┌─────────────────┐                    ┌─────────────────┐
│  COMPUTADORA 1  │                    │  COMPUTADORA 2  │
│    (Servidor)   │                    │    (Cliente)    │
└─────────────────┘                    └─────────────────┘
         │                                      │
         │  1. Instalar ngrok                   │  1. run_client.bat
         │  2. run_server_online.bat            │  2. Conectar → Online
         │  3. Copiar URL ngrok                 │  3. Ingresar URL
         │  4. Compartir con jugador 2 ──────►  │  4. Conectar
         │  5. run_client.bat                   │
         │  6. Conectar → LAN (localhost)       │
         │                                      │
         └──────────────────────────────────────┘
                  Internet (ngrok)
```

---

## 📋 Checklist Pre-Juego

### ✅ Para Juego LAN:
- [ ] Python instalado
- [ ] pygame instalado (`pip install pygame`)
- [ ] Ambos en la misma WiFi
- [ ] Servidor iniciado (`run_server.bat`)
- [ ] Firewall de Windows permite Python

### ✅ Para Juego Online:
- [ ] Python instalado
- [ ] pygame instalado
- [ ] requests instalado (`pip install requests`)
- [ ] ngrok descargado (https://ngrok.com/download)
- [ ] ngrok.exe en carpeta del juego
- [ ] Servidor online iniciado (`run_server_online.bat`)
- [ ] URL de ngrok compartida con jugador 2

---

## 🎯 Pantallas del Juego

### 1. Pantalla de Conexión
```
╔═══════════════════════════════════════╗
║  Configuración de Conexión            ║
╠═══════════════════════════════════════╣
║                                       ║
║  Modo:  [LAN (Local)] [Online(ngrok)]║
║                                       ║
║  Host:  [________________]            ║
║  Puerto:[________________]            ║
║                                       ║
║  [Conectar]  [Cancelar]               ║
╚═══════════════════════════════════════╝
```

### 2. Menú Principal
```
╔═══════════════════════════════════════╗
║         BATALLA NAVAL                 ║
╠═══════════════════════════════════════╣
║                                       ║
║      [Conectar a Servidor]            ║
║                                       ║
║      [Iniciar Partida]                ║
║                                       ║
║  Estado: Desconectado del servidor    ║
╚═══════════════════════════════════════╝
```

### 3. Fase de Colocación
```
╔═══════════════════════════════════════╗
║  Coloca tus barcos                    ║
╠═══════════════════════════════════════╣
║   A B C D E F G H I J                 ║
║ 1 □ □ □ □ □ □ □ □ □ □                 ║
║ 2 □ □ □ □ □ □ □ □ □ □                 ║
║ 3 □ □ ■ ■ ■ ■ ■ □ □ □  ← Portaaviones ║
║ 4 □ □ □ □ □ □ □ □ □ □                 ║
║   ...                                 ║
║                                       ║
║  [R] Rotar | Click para colocar       ║
╚═══════════════════════════════════════╝
```

### 4. Fase de Batalla
```
╔═══════════════════════════════════════════════════════╗
║  TU TABLERO           TABLERO ENEMIGO                 ║
╠═══════════════════════════════════════════════════════╣
║  A B C D E ...        A B C D E ...                   ║
║1 ■ □ ✕ □ □ ...      1 ○ □ □ ✕ □ ...                  ║
║2 ■ □ □ ○ □ ...      2 □ □ □ □ □ ...                  ║
║3 ■ ✕ □ □ □ ...      3 □ ✕ □ □ □ ...                  ║
║  ...                   ...                            ║
║                                                       ║
║  Turno: TU TURNO - Dispara al tablero enemigo         ║
╚═══════════════════════════════════════════════════════╝

Leyenda:
□ = Agua
■ = Tu barco
✕ = Impacto (hit)
○ = Agua disparada (miss)
```

---

## 🔧 Comandos de Terminal Útiles

```bash
# Verificar Python
python --version

# Verificar ngrok
ngrok version

# Instalar dependencias
pip install -r requirements.txt

# Verificar IP local (para LAN)
ipconfig

# Matar procesos Python (si algo queda colgado)
taskkill /F /IM python.exe

# Matar ngrok
taskkill /F /IM ngrok.exe
```

---

## 🆘 Solución Rápida

| Problema | Solución Rápida |
|----------|----------------|
| No inicia el juego | Ejecutar `install_and_run.ps1` |
| No se ve ngrok | Descargar de ngrok.com y copiar a carpeta |
| No conecta en LAN | Verificar `ipconfig` y usar IP local |
| No conecta online | Copiar exactamente URL de ngrok |
| Error de pygame | `pip install pygame` |
| Error de requests | `pip install requests` |
| Firewall bloquea | Permitir Python en Firewall de Windows |

---

## 📞 Ayuda Adicional

- **Inicio Rápido**: `INICIO_RAPIDO.md`
- **Guía Completa Online**: `GUIA_JUEGO_ONLINE.md`
- **Instalador**: `INSTALADOR_README.md`

---

## 🎊 ¡Listo!

```
     🚢 
    ~~~
   ~~~~~
  ⚓~~~~⚓
 ~~~~~~~~~
¡BATALLA NAVAL!
```

**¡A hundir barcos!** ⚓🎯

---

**Tip Pro**: Usa `run_server_online.bat` para jugar con amigos de otras ciudades/países! 🌍
