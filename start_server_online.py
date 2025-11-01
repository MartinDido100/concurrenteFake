"""
Script para iniciar el servidor con soporte para ngrok (juego online)
Detecta automáticamente si ngrok está instalado y lo configura
"""

import asyncio
import subprocess
import time
import sys
import os
import json
import threading
import requests
from server import main as server_main

class NgrokManager:
    def __init__(self, port=8888):
        self.port = port
        self.ngrok_process = None
        self.public_url = None
        
    def check_ngrok_installed(self):
        """Verificar si ngrok está instalado"""
        try:
            result = subprocess.run(['ngrok', 'version'], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=5)
            if result.returncode == 0:
                print(f"✅ ngrok encontrado: {result.stdout.strip()}")
                return True
        except FileNotFoundError:
            print("❌ ngrok no está instalado")
            return False
        except Exception as e:
            print(f"❌ Error verificando ngrok: {e}")
            return False
        return False
    
    def start_ngrok(self):
        """Iniciar túnel ngrok"""
        try:
            print(f"🚀 Iniciando túnel ngrok en puerto {self.port}...")
            
            # Iniciar ngrok en modo TCP
            self.ngrok_process = subprocess.Popen(
                ['ngrok', 'tcp', str(self.port), '--log=stdout'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Esperar un momento para que ngrok se inicie
            time.sleep(3)
            
            # Obtener la URL pública desde la API de ngrok
            self.public_url = self.get_ngrok_url()
            
            if self.public_url:
                print("=" * 80)
                print(f"✅ TÚNEL NGROK ACTIVO")
                print("=" * 80)
                print(f"🌐 URL pública de ngrok: {self.public_url}")
                print("=" * 80)
                print(f"📋 Los jugadores deben usar esta información para conectarse:")
                host, port = self.parse_ngrok_url(self.public_url)
                print(f"   Host: {host}")
                print(f"   Puerto: {port}")
                print("=" * 80)
                return True
            else:
                print("❌ No se pudo obtener la URL de ngrok")
                self.stop_ngrok()
                return False
                
        except FileNotFoundError:
            print("❌ ngrok no encontrado. Por favor instálalo desde: https://ngrok.com/download")
            return False
        except Exception as e:
            print(f"❌ Error iniciando ngrok: {e}")
            return False
    
    def get_ngrok_url(self):
        """Obtener URL pública desde la API local de ngrok"""
        max_attempts = 10
        for attempt in range(max_attempts):
            try:
                response = requests.get('http://localhost:4040/api/tunnels', timeout=2)
                if response.status_code == 200:
                    tunnels = response.json()['tunnels']
                    if tunnels:
                        # Buscar el túnel TCP
                        for tunnel in tunnels:
                            if tunnel['proto'] == 'tcp':
                                return tunnel['public_url']
                        # Si no hay TCP, usar el primero disponible
                        return tunnels[0]['public_url']
            except requests.exceptions.RequestException:
                if attempt < max_attempts - 1:
                    print(f"⏳ Esperando ngrok... (intento {attempt + 1}/{max_attempts})")
                    time.sleep(2)
                else:
                    print("❌ No se pudo conectar a la API de ngrok")
        return None
    
    def parse_ngrok_url(self, url):
        """Parsear URL de ngrok para extraer host y puerto"""
        # Formato: tcp://0.tcp.ngrok.io:12345
        if url.startswith('tcp://'):
            url = url[6:]  # Quitar 'tcp://'
            if ':' in url:
                host, port = url.rsplit(':', 1)
                return host, int(port)
        return None, None
    
    def stop_ngrok(self):
        """Detener túnel ngrok"""
        if self.ngrok_process:
            print("🛑 Deteniendo túnel ngrok...")
            self.ngrok_process.terminate()
            try:
                self.ngrok_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.ngrok_process.kill()
            self.ngrok_process = None
            print("✅ Túnel ngrok detenido")

def print_banner():
    """Mostrar banner del servidor"""
    print("\n" + "=" * 80)
    print("🚢 BATALLA NAVAL - SERVIDOR ONLINE (con ngrok)")
    print("=" * 80)
    print("Este servidor permite conexiones desde cualquier parte del mundo")
    print("usando ngrok como túnel seguro.")
    print("=" * 80 + "\n")

def print_instructions():
    """Mostrar instrucciones"""
    print("\n" + "=" * 80)
    print("📋 INSTRUCCIONES:")
    print("=" * 80)
    print("1. El servidor se iniciará automáticamente en el puerto 8888")
    print("2. ngrok creará un túnel público hacia tu servidor local")
    print("3. Comparte la URL de ngrok (host y puerto) con otros jugadores")
    print("4. Los jugadores deben ingresar estos datos en el cliente")
    print("5. ¡A jugar!")
    print("\n⚠️  IMPORTANTE:")
    print("   - Mantén esta ventana abierta mientras juegues")
    print("   - La URL de ngrok cambia cada vez que reinicias el servidor")
    print("   - Versión gratuita de ngrok tiene límites de conexiones")
    print("=" * 80 + "\n")

def check_ngrok_installation():
    """Verificar e informar sobre la instalación de ngrok"""
    print("🔍 Verificando instalación de ngrok...")
    
    ngrok = NgrokManager()
    if not ngrok.check_ngrok_installed():
        print("\n" + "=" * 80)
        print("⚠️  NGROK NO ESTÁ INSTALADO")
        print("=" * 80)
        print("\nPara jugar online, necesitas instalar ngrok:")
        print("\n📥 PASOS PARA INSTALAR NGROK:")
        print("   1. Ve a: https://ngrok.com/download")
        print("   2. Descarga ngrok para Windows")
        print("   3. Extrae el archivo ngrok.exe")
        print("   4. Opción A: Coloca ngrok.exe en esta carpeta")
        print("   5. Opción B: Agrega ngrok.exe al PATH de Windows")
        print("\n📝 AGREGAR AL PATH (Opcional pero recomendado):")
        print("   1. Busca 'Variables de entorno' en Windows")
        print("   2. Edita la variable 'Path' del usuario")
        print("   3. Agrega la ruta donde está ngrok.exe")
        print("\n🔐 AUTENTICACIÓN (Recomendado):")
        print("   1. Crea cuenta gratis en: https://dashboard.ngrok.com/signup")
        print("   2. Copia tu token de autenticación")
        print("   3. Ejecuta: ngrok authtoken TU_TOKEN")
        print("=" * 80)
        
        input("\n⏸️  Presiona Enter después de instalar ngrok para continuar...")
        
        # Verificar nuevamente
        if not ngrok.check_ngrok_installed():
            print("\n❌ ngrok aún no está instalado correctamente")
            print("🔄 Opciones:")
            print("   1. Continuar sin ngrok (solo LAN)")
            print("   2. Salir e instalar ngrok")
            
            choice = input("\n¿Continuar sin ngrok? (s/N): ").strip().lower()
            if choice != 's':
                print("👋 Saliendo... Instala ngrok y vuelve a intentar")
                sys.exit(0)
            return None
    
    return ngrok

async def run_server_with_ngrok():
    """Ejecutar servidor con ngrok"""
    print_banner()
    
    # Verificar ngrok
    ngrok = check_ngrok_installation()
    
    if ngrok:
        print_instructions()
        
        # Iniciar ngrok
        if not ngrok.start_ngrok():
            print("\n❌ Error iniciando ngrok")
            print("🔄 Continuando con servidor local solamente...")
            ngrok = None
    
    print("\n" + "=" * 80)
    print("🎯 INICIANDO SERVIDOR...")
    print("=" * 80 + "\n")
    
    try:
        # Iniciar servidor
        await server_main()
    except KeyboardInterrupt:
        print("\n\n🛑 Servidor detenido por el usuario")
    except Exception as e:
        print(f"\n❌ Error en el servidor: {e}")
    finally:
        # Detener ngrok si está activo
        if ngrok:
            ngrok.stop_ngrok()
        print("\n👋 Servidor cerrado")

def main():
    """Función principal"""
    try:
        asyncio.run(run_server_with_ngrok())
    except KeyboardInterrupt:
        print("\n👋 Adiós")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
