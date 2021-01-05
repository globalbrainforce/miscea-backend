""" APP """
import asyncio
import json
import logging
import websockets

# from events.auth import auth
from events.auth import auth

logging.basicConfig()

USERS = set()

async def app(websocket, path):
    """ MAIN APPLICATION """

    USERS.add(websocket)

    try:

        async for message in websocket:

            data = json.loads(message)

            if path == '/auth':

                await auth.auth(USERS, data)

    finally:

        USERS.remove(websocket)

MAIN = websockets.serve(app, "0.0.0.0", 6789)

asyncio.get_event_loop().run_until_complete(MAIN)
asyncio.get_event_loop().run_forever()
