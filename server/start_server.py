#!/usr/bin/env python3
"""
Script para iniciar el servidor de Batalla Naval sin ngrok
Versión para VM con configuración de host y puerto
"""

import asyncio
import argparse
import sys
import os
import signal

# Agregar el directorio padre al path para importar constants compartido
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from server import main as server_main
from constants import *

class SimpleServer:
    def __init__(self, host='0.0.0.0', port=DEFAULT_SERVER_PORT):
        self.host = host
        self.port = port
        self.running = False
        
    def print_banner(self):
        """Mostrar banner del servidor"""
        print("\n" + "=" * 80)
        print("🚢 BATALLA NAVAL - SERVIDOR DIRECTO")
        print("=" * 80)
        print("Servidor configurado para recibir conexiones directas")
        print("Sin dependencias de ngrok - ideal para VM/VPS")
        print("=" * 80 + "\n")

    def print_server_info(self):
        """Mostrar información del servidor"""
        print("📋 CONFIGURACIÓN DEL SERVIDOR:")
        print("=" * 80)
        print(f"🌐 Host: {self.host}")
        print(f"🔌 Puerto: {self.port}")
        print(f"🔗 URL de conexión: {self.host}:{self.port}")
        
        if self.host == '0.0.0.0':
            print("\n🌍 ACCESO PÚBLICO:")
            print("   - El servidor escucha en TODAS las interfaces de red")
            print("   - Los clientes pueden conectarse desde cualquier IP")
            print("   - Asegúrate de que el puerto esté abierto en el firewall")
            
        print("\n📝 INSTRUCCIONES PARA CLIENTES:")
        print("   1. Los jugadores deben usar la IP pública de esta máquina")
        print(f"   2. Puerto a configurar en el cliente: {self.port}")
        print("   3. Formato de conexión: <IP_PUBLICA>:<PUERTO>")
        print("=" * 80 + "\n")

    def print_firewall_instructions(self):
        """Mostrar instrucciones de firewall"""
        print("🔥 CONFIGURACIÓN DE FIREWALL (Linux):")
        print("=" * 80)
        print(f"sudo ufw allow {self.port}")
        print("sudo ufw reload")
        print()
        print("🔥 CONFIGURACIÓN DE FIREWALL (CentOS/RHEL):")
        print(f"sudo firewall-cmd --permanent --add-port={self.port}/tcp")
        print("sudo firewall-cmd --reload")
        print("=" * 80 + "\n")

    async def start(self):
        """Iniciar el servidor"""
        self.print_banner()
        self.print_server_info()
        self.print_firewall_instructions()
        
        print("🚀 INICIANDO SERVIDOR...")
        print("=" * 80)
        print("⏸️  Presiona Ctrl+C para detener el servidor")
        print("💡 Mantén esta ventana abierta mientras el servidor esté activo")
        print("=" * 80 + "\n")
        
        self.running = True
        
        try:
            # Crear el servidor con la configuración especificada
            from server import BattleshipServer
            server = BattleshipServer(host=self.host, port=self.port)
            await server.start_server()
            
        except OSError as e:
            if "Address already in use" in str(e):
                print(f"❌ ERROR: El puerto {self.port} ya está en uso")
                print("💡 Soluciones:")
                print("   1. Usar un puerto diferente: --port OTRO_PUERTO")
                print("   2. Detener el proceso que usa el puerto")
                print(f"   3. Encontrar proceso: sudo lsof -i :{self.port}")
            else:
                print(f"❌ ERROR de red: {e}")
            sys.exit(1)
            
        except KeyboardInterrupt:
            print("\n\n🛑 Servidor detenido por el usuario")
            
        except Exception as e:
            print(f"\n❌ Error inesperado: {e}")
            sys.exit(1)
            
        finally:
            self.running = False
            print("\n👋 Servidor cerrado correctamente")

def setup_signal_handlers(server_instance):
    """Configurar manejadores de señales para cierre limpio"""
    def signal_handler(signum, frame):
        print(f"\n🔔 Señal recibida: {signum}")
        print("🛑 Deteniendo servidor...")
        server_instance.running = False
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

def validate_args(args):
    """Validar argumentos de línea de comandos"""
    # Validar puerto
    if not (1 <= args.port <= 65535):
        print(f"❌ Error: Puerto {args.port} fuera de rango válido (1-65535)")
        sys.exit(1)
    
    # Validar host
    if args.host not in ['0.0.0.0', 'localhost', '127.0.0.1'] and not args.host.replace('.', '').isdigit():
        print(f"⚠️  Advertencia: Host '{args.host}' podría no ser válido")
        response = input("¿Continuar de todos modos? (s/N): ").strip().lower()
        if response != 's':
            sys.exit(0)

def main():
    """Función principal"""
    parser = argparse.ArgumentParser(
        description='Servidor de Batalla Naval sin ngrok',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  %(prog)s                          # Usar configuración por defecto
  %(prog)s --port 9000              # Usar puerto específico
  %(prog)s --host 192.168.1.100     # Usar IP específica
  %(prog)s --host 0.0.0.0 --port 8080 # Configuración para VPS/VM

Configuración por defecto:
  Host: 0.0.0.0 (todas las interfaces)
  Puerto: """ + str(DEFAULT_SERVER_PORT)
    )
    
    parser.add_argument(
        '--host', 
        default='0.0.0.0',
        help='Host/IP en la que escuchar (default: 0.0.0.0 para todas las interfaces)'
    )
    
    parser.add_argument(
        '--port', 
        type=int, 
        default=DEFAULT_SERVER_PORT,
        help=f'Puerto en el que escuchar (default: {DEFAULT_SERVER_PORT})'
    )
    
    parser.add_argument(
        '--version', 
        action='version', 
        version='Batalla Naval Server v1.0'
    )
    
    args = parser.parse_args()
    
    # Validar argumentos
    validate_args(args)
    
    # Crear instancia del servidor
    server = SimpleServer(host=args.host, port=args.port)
    
    # Configurar manejadores de señales
    setup_signal_handlers(server)
    
    # Iniciar servidor
    try:
        asyncio.run(server.start())
    except KeyboardInterrupt:
        print("\n👋 Servidor interrumpido")
    except Exception as e:
        print(f"❌ Error fatal: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()