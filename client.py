import asyncio
import websockets
import json


async def play():
    async with websockets.connect(
            'ws://localhost:8765') as websocket:
        finished = False
        print("1) Play with other player (in development)")
        print("2) Training mode")
        mode = input("Choose mode:")
        await websocket.send(mode.strip())
        if mode == '1':
            res = await websocket.recv()
            print(f"{res}")
            number = input("Type your number: ")
            await websocket.send(number.strip())
        while finished is False:
            guess = input("Guess the number: ")
            await websocket.send(guess.strip())

            res = json.loads(await websocket.recv())
            finished = res['finished']
            if not res['message']:
                print(f"< Guessed: {res['guessed']}")
                print(f"< Placed: {res['placed']}")
            else:
                print(f"< {res['message']}")

asyncio.get_event_loop().run_until_complete(play())
