""" APP """
import syslog
import asyncio
import json
import logging
import websockets

from events.auth import auth
from events.message import message

logging.basicConfig()

USERS = {}

async def app(websocket, path):
    """ MAIN APPLICATION """

    # USERS.add(websocket)

    try:

        async for webs in websocket:

            data = json.loads(webs)

            if path == '/auth':

                await auth.auth(websocket, data)

            if path == '/message':

                if await message.message(websocket, data):

                    websocket_id = data['system_id']

                    if not websocket_id in USERS.keys():

                        USERS[websocket_id] = websocket

                    log_sys = "USERS: {0}".format(USERS)
                    syslog.syslog(log_sys)
    finally:

        new_users = {}

        for key in USERS.keys():

            if not USERS[key] == websocket:

                new_users[key] = USERS[key]

        USERS = new_users
        log_sys = "New USERS: {0}".format(USERS)
        syslog.syslog(log_sys)

MAIN = websockets.serve(app, "0.0.0.0", 6789)

asyncio.get_event_loop().run_until_complete(MAIN)
asyncio.get_event_loop().run_forever()
