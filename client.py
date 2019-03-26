import asyncio
import websockets
import json


async def play():
    async with websockets.connect(
            'ws://localhost:8765') as websocket:
        
        print("1) Play with other player")
        print("2) Training mode")
        mode = input("Choose mode:")
        websocket.send(mode.strip())
        if mode == 1:
            number = input("Type your number: ")
            websocket.send(number.strip())
        while True:
            guess = input("Guess the number: ")
            await websocket.send(guess.strip())

            res = json.loads(await websocket.recv())
            if not res['message']:
                print(f"< Guessed: {res['guessed']}")
                print(f"< Placed: {res['placed']}")
            else:
                print(f"< {res['message']}")

asyncio.get_event_loop().run_until_complete(play())
asyncio.get_event_loop().run_forever()