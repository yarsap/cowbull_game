import asyncio
import json
import random
import websockets

import game
from constants import DIGITS

connected = set()

# async def handler(websocket, path):
#     # Register.
#     connected.add(websocket)
#     try:
#         # Implement logic here.
#         await asyncio.wait([ws.send("Hello!") for ws in connected])
#         await asyncio.sleep(10)
#     finally:
#         # Unregister.
#         connected.remove(websocket)

async def play(websocket, path):

    connected.add(websocket)
    print ("Training mode!")
    print(f"Connected players: {[client.remote_address[1] for client in connected]}")
    guessed = False
    number = ''.join(random.sample(DIGITS, 4))

    # import pdb; pdb.set_trace()
    while not guessed:
        try:
            print(f"< {number}")

            guess = await websocket.recv()

            print(f"< {guess}")
            if game.validate_entry(guess):
                res = game.check(guess, number)
                guessed = res['finished']
                if guessed:
                    res['message'] = "Congratulations! You win!"
            
            else:
                res = {'message': "Invalid input"}
            
            
            await websocket.send(json.dumps(res))
            print(f"> {res}")
        finally:
            connected.remove(websocket)

print ("Hello! I'm a cowbull server!")
start_server = websockets.serve(play, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()