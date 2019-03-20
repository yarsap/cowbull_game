#!/usr/bin/env python

import asyncio
import websockets
import json


async def play():
    async with websockets.connect(
            'ws://localhost:8765') as websocket:
        while True:
            guess = input("Guess the number: ")
            await websocket.send(guess)

            res = json.loads(await websocket.recv())

            print(f"< Guessed: {res['guessed']}")
            print(f"< Placed: {res['placed']}")

# asyncio.get_event_loop().run_until_complete(hello())
asyncio.get_event_loop().run_until_complete(play())
# asyncio.get_event_loop().run_forever()