import asyncio
import json
import random

from constants import DIGITS

def check(guess, target):
    guessed = 0
    placed = 0
    for idx, digit in enumerate(guess):
        if digit in target:
            guessed+=1
        
        if digit is target[idx]:
            placed+=1
    
    return {'guessed': guessed,
            'placed': placed,
            'finished': guessed == placed == 4,
            'message': None}
        

def validate_entry(user_input):
    if len(user_input) != 4:
        return False
    
    for i in user_input:
        if user_input.count(i) > 1:
            return False
        
        if i not in DIGITS:
            return False
    
    return True

async def play_multi(websocket_pair):

    player_1 = websocket_pair[0]
    player_2 = websocket_pair[1]

    player_numbers = {
        player_1.remote_address[1]: None,
        player_2.remote_address[1]: None,
    }

    for player in websocket_pair:
        await player.send()
    
    number_1 = await player_1.recv()
    number_2 = await player_2.recv()

    # while not validate_entry(number):
    #     await player.send("Invalid input")
    #     number = await player.recv()

    # numbers inversed for easier access in loop
    player_numbers[player_1.remote_address[1]] = number_2
    player_numbers[player_2.remote_address[1]] = number_1


    while True:
        for player in websocket_pair:
            print(f"< {player_numbers[player.remote_address[1]]}")

            guess = await player.recv()

            print(f"< {guess}")
            if validate_entry(guess):
                res = check(guess, player_numbers[player.remote_address[1]])
                guessed = res['finished']
                if guessed:
                    res['message'] = "Congratulations! You win!"
            
            else:
                res = {'message': "Invalid input"}
            
            
            await player.send(json.dumps(res))
            print(f"> {res}")



async def play_single(websocket):
    print ("Training mode!")
    number = ''.join(random.sample(DIGITS, 4))
    guessed = False
    while not guessed:
        
        print(f"< {number}")

        guess = await websocket.recv()

        print(f"< {guess}")
        if validate_entry(guess):
            res = check(guess, number)
            guessed = res['finished']
            if guessed:
                res['message'] = "Congratulations! You win!"
        
        else:
            res = {'message': "Invalid input"}
        
        
        await websocket.send(json.dumps(res))
        print(f"> {res}")