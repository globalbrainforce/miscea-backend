""" APP """
import asyncio
import json
import logging
import websockets

from events.auth import auth
from events.message import message

logging.basicConfig()

USERS = set()

async def app(websocket, path):
    """ MAIN APPLICATION """

    # USERS.add(websocket)

    try:

        async for webs in websocket:

            data = json.loads(webs)

            if path == '/auth':

                if await auth.auth(websocket, data):

                    USERS.add(websocket)

            if path == '/message':

                if await message.message(websocket, data):

                    USERS.add(websocket)

    finally:

        USERS.remove(websocket)

MAIN = websockets.serve(app, "0.0.0.0", 6789)

asyncio.get_event_loop().run_until_complete(MAIN)
asyncio.get_event_loop().run_forever()
