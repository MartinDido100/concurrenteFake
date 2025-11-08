"""
Cliente asíncrono para el juego Batalla Naval
Maneja la comunicación de red con el servidor usando asyncio
"""

import asyncio
import sys
import os

# Importar constants desde la carpeta padre del proyecto
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from constants import *

class Client:
    def __init__(self):
        self.connected = True
        self.reader = None
        self.writer = None

    async def listen_server(self):
        """Tarea asíncrona que escucha mensajes del servidor"""
        try:
            while self.connected and self.reader:
                # Recibir respuesta del servidor de forma asíncrona
                data = await self.reader.read(NETWORK_BUFFER_SIZE)
                
                if not data:
                    # El servidor cerró la conexión
                    print("\n🔌 El servidor cerró la conexión")
                    self.connected = False
                    break
                
                response = data.decode("ascii").strip()
                
                # Mostrar la respuesta del servidor
                print(f"\n📨 {response}")
                print("> ", end="", flush=True)  # Mostrar prompt nuevamente
                
        except asyncio.CancelledError:
            # Tarea cancelada normalmente
            pass
        except ConnectionResetError:
            print("\n🚨 Conexión perdida: El servidor se desconectó inesperadamente")
            self.connected = False
        except Exception as e:
            print(f"\n❌ Error recibiendo datos: {e}")
            self.connected = False

    async def send_messages(self):
        """Tarea asíncrona para enviar mensajes al servidor"""
        try:
            while self.connected and self.writer:
                # Usar asyncio para input no bloqueante
                loop = asyncio.get_event_loop()
                envie = await loop.run_in_executor(None, input, "> ")        
                if not self.connected:
                    break

                # Enviar mensaje al servidor
                self.writer.write(envie.encode("ascii"))
                await self.writer.drain()
                if envie == "fin":
                    print("🚪 Desconectando...")
                    break            
        except asyncio.CancelledError:
            # Tarea cancelada normalmente
            pass
        except KeyboardInterrupt:
            print("\n⚠️ Interrumpido por el usuario")
            self.connected = False
        except ConnectionResetError:
            print("\n🚨 Error: El servidor cerró la conexión")
            self.connected = False
        except Exception as e:
            print(f"\n❌ Error enviando mensaje: {e}")
            self.connected = False

    async def client(self):
        """Cliente principal asíncrono"""
        try:
            print("🔄 Conectando al servidor...")
            
            # Crear conexión asíncrona
            self.reader, self.writer = await asyncio.open_connection(DEFAULT_SERVER_HOST, DEFAULT_SERVER_PORT)
            
            print(f"✅ Conectado al servidor en {DEFAULT_SERVER_HOST}:{DEFAULT_SERVER_PORT}")
            print("💡 Escribe 'fin' para desconectarte")
            print("💡 El cliente se cerrará automáticamente si el servidor se desconecta")
            
            # Crear tareas asíncronas para escuchar y enviar
            listen_task = asyncio.create_task(self.listen_server())
            send_task = asyncio.create_task(self.send_messages())
            
            # Esperar a que cualquiera de las dos tareas termine
            done, pending = await asyncio.wait( #la que quede pendiente se cancela
                [listen_task, send_task],
                return_when=asyncio.FIRST_COMPLETED
            )
            
            # Cancelar la tarea pendiente
            for task in pending:
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
            
        except ConnectionRefusedError:
            print("❌ Error: No se puede conectar al servidor")
            print("   Asegúrate de que el servidor esté ejecutándose")
        except Exception as e:
            print(f"❌ Error de conexión: {e}")
        finally:
            print("🔚 Cliente finalizado")
            self.connected = False
            # Cerrar escritor si existe
            if self.writer:
                try:
                    self.writer.close()
                    await self.writer.wait_closed()
                except Exception as e:
                    print(f"Error closing writer: {e}")

async def client_main():
    """Función principal del cliente"""
    client = Client()
    try:
        await client.client()
    except KeyboardInterrupt:
        print("\n⚠️ Cliente interrumpido por el usuario")
    except Exception as e:
        print(f"❌ Error inesperado en el cliente: {e}")
    finally:
        print("👋 ¡Adiós!")