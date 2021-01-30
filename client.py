import asyncio
import websockets
import json

from constants import DIGITS

def validate_entry(user_input):
    if len(user_input) != 4:
        return False
    
    for i in user_input:
        if user_input.count(i) > 1:
            return False
        
        if i not in DIGITS:
            return False
    
    return True

async def play():
    async with websockets.connect(
            'ws://localhost:8765', ping_interval=None) as websocket:
        finished = False
        print("1) Play with other player (in development)")
        print("2) Training mode")
        mode = input("Choose mode:")
        await websocket.send(mode.strip())
        if mode == '1':
            # res = await websocket.recv()
            # print(f"{res}")
            number = input("Type your number: ")
            while not validate_entry(number):
                print("Invalid input")
                number = input("Type your number: ")
            await websocket.send(number.strip())
        while finished is False:
            guess = input("Guess the number: ")
            await websocket.send(guess.strip())

            res = json.loads(await websocket.recv())
            finished = res["finished"]
            if not res["message"]:
                print(f"< Guessed: {res['guessed']}")
                print(f"< Placed: {res['placed']}")
            else:
                print(f"< {res['message']}")

asyncio.get_event_loop().run_until_complete(play())
