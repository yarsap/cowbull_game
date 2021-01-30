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
    idle_players.difference_update(players)
    return players

async def register_connected(websocket):
    connected.add(websocket)

async def register_idle(websocket):
    idle_players.add(websocket)
    # await notify_users()

async def notify_users():
    if idle_players:
        message = str(idle_players)
        await asyncio.wait([user.send(message) for user in idle_players])

async def play(websocket, path):
    # await register_connected(websocket)
    mode = await websocket.recv()

    if mode == '1':
        await register_idle(websocket)
        print(idle_players)
        while len(idle_players) < 2:
            await asyncio.sleep(1)
            websocket.send("Waiting for other player...\n")
        websocket.send("Match found")
        ws = make_match(idle_players)
    else:
        ws = websocket

    try:
        await play_modes[mode](ws)
    finally:
        # connected.remove(websocket)
        websocket.close()

print ("Hello! I'm a cowbull server!")
start_server = websockets.serve(play, 'localhost', 8765, ping_interval=None)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()