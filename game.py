import asyncio
import json
import random

from constants import DIGITS, WIN_MSG, LOSE_MSG, TIE_MSG

def check(guess, target):
    guessed = 0
    placed = 0
    for idx, digit in enumerate(guess):
        if digit in target:
            guessed+=1
        
        if digit is target[idx]:
            placed+=1
    
    return {"guessed": guessed,
            "placed": placed,
            "finished": guessed == placed == 4,
            "message": None}
        

async def play_multi(websocket_pair):

    player_1, player_2 = websocket_pair

    player_numbers = {
        player_1.remote_address[1]: None,
        player_2.remote_address[1]: None,
    }

    numbers = await asyncio.gather(player_1.recv(), player_2.recv())
    player_numbers[player_1.remote_address[1]] = numbers[1]
    player_numbers[player_2.remote_address[1]] = numbers[0]

    finished = False
    while not finished:
        guesses = await asyncio.gather(player_1.recv(), player_2.recv())

        print(f"< {player_1.remote_address[1]} - {guesses[0]}")
        print(f"< {player_2.remote_address[1]} - {guesses[1]}")
        res_1 = check(guesses[0], player_numbers[player_1.remote_address[1]])
        res_2 = check(guesses[1], player_numbers[player_2.remote_address[1]])
        if res_1["finished"] and res_2["finished"]:
            res_1["message"] = TIE_MSG
            res_2["message"] = TIE_MSG
            finished = True
        elif res_1["finished"]:
            res_1["message"] = WIN_MSG
            res_2["message"] = LOSE_MSG
            res_2["finished"] = True
            finished = True
        elif res_2["finished"]:
            res_2["message"] = WIN_MSG
            res_1["message"] = LOSE_MSG
            res_1["finished"] = True
            finished = True
        await asyncio.wait([player_1.send(json.dumps(res_1)), player_2.send(json.dumps(res_2))])
        print(f"> {player_1.remote_address[1]} - {res_1}")
        print(f"> {player_2.remote_address[1]} - {res_2}")


async def play_single(websocket):
    print ("Training mode!")
    number = ''.join(random.sample(DIGITS, 4))
    finished = False
    while not finished:
        print(f"< {number}")
        guess = await websocket.recv()
        print(f"< {guess}")
      
        res = check(guess, number)
        finished = res["finished"]
        if finished:
            res["message"] = WIN_MSG
          
        await websocket.send(json.dumps(res))
        print(f"> {res}")