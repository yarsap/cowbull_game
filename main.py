#!/usr/bin/env python

# WS server example

import asyncio
import websockets
import game
import json
import random
import string

async def play(websocket, path):
    
    number = ''.join(random.sample(string.digits, 4))
    print(f"< {number}")
    guess = await websocket.recv()
    print(f"< {guess}")

    res = game.check(guess, number)

    await websocket.send(json.dumps(res))
    print(f"> {res}")

start_server = websockets.serve(play, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()