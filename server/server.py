import asyncio
import logging
import sys
import os

# Agregar la carpeta classes al path
#esto capaz se puede cambiar porque el server lo hosteamos con una vm, entonces
# no tiene sentido que todo este en el mismo lado
#preguntar al profe como hacer porque duplicamos la clase barco en server y cliente
#o lo hacemos como si fuera local o si no nose

sys.path.append(os.path.join(os.path.dirname(__file__), 'classes'))

# Agregar el directorio padre al path para importar constants compartido
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from battleship_server import BattleshipServer
from constants import *

# Configurar logging
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

async def main():
    server = BattleshipServer()
    try:
        await server.start_server()
    except KeyboardInterrupt:
        logger.info("Servidor detenido por el usuario")
    except Exception as e:
        logger.error(f"Error en el servidor: {e}")

if __name__ == "__main__":
    asyncio.run(main())