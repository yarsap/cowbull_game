import asyncio
import json
import random
import websockets

import game
from constants import DIGITS


async def play(websocket, path):
    number = ''.join(random.sample(DIGITS, 4))
    print(f"< {number}")
    guess = await websocket.recv()
    print(f"< {guess}")

    res = json.dumps(game.check(guess, number))

    await websocket.send(res)
    print(f"> {res}")

start_server = websockets.serve(play, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()