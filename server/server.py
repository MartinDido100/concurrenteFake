import asyncio
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'classes'))

sys.path.append(os.path.dirname(__file__))

from battleship_server import BattleshipServer
from constants import *

async def main():
    server = BattleshipServer()
    try:
        await server.start_server()
    except Exception as e:
        pass

if __name__ == "__main__":
    asyncio.run(main())