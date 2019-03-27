import asyncio
import websockets
import random

import game

play_modes = {
    '1': game.play_multi,
    '2': game.play_single
}

connected = set()
idle_players = set()

def make_match(players_set):
    players = random.sample(players_set, 2)
    players_set.remove(players)
    return players

async def play(websocket, path):

    connected.add(websocket)

    print(f"Connected players: {[client.remote_address[1] for client in connected]}")

    mode = await websocket.recv()

    if mode == '1':
        idle_players.add(websocket)

        websocket.send("Waiting for other player...")
        while len(idle_players) < 2:
            asyncio.sleep(10)
        else:
            ws = make_match(idle_players)
    else:
        ws = websocket

    try:
        await play_modes[mode](ws)
    finally:
        connected.remove(websocket)

print ("Hello! I'm a cowbull server!")
start_server = websockets.serve(play, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()