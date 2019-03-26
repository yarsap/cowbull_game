import asyncio
import websockets
import random

import game

play_modes = {
    1: game.play_multi,
    2: game.play_single
}

connected = set()
idle_players = set()

def make_match(players_set):
    player_1 = random.choice(players_set)
    players_set.remove(player_1)
    player_2 = random.choice(players_set)
    players_set.remove(player_2)
    return (player_1, player_2)

async def play(websocket, path):

    connected.add(websocket)

    print(f"Connected players: {[client.remote_address[1] for client in connected]}")
    guessed = False
    mode = await websocket.recv()
    if mode == '1':
        idle_players.add(websocket)
        await websocket.send("Waiting for other player...")
        while len(idle_players) < 2:
            await asyncio.sleep(10)
        else:
            ws = make_match(idle_players)
    else:
        ws = websocket
    # import pdb; pdb.set_trace()
    try:
        play_modes[mode](ws)
    finally:
        connected.remove(websocket)

print ("Hello! I'm a cowbull server!")
start_server = websockets.serve(play, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()