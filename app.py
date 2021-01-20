""" APP """
import syslog
import asyncio
import json
import logging
import websockets

from events.auth import auth
from events.message import message

logging.basicConfig()

USERS = []

async def app(websocket, path):
    """ MAIN APPLICATION """

    # USERS.add(websocket)

    try:

        async for webs in websocket:

            data = json.loads(webs)

            if path == '/auth':

                if await auth.auth(websocket, data):

                    new_user = {}
                    new_user['system_id'] = data['system_id']
                    new_user['websocket'] = websocket

                    USERS.append(new_user)
                    # USERS.add(websocket)
                    log_sys = "USERS: {0}".format(USERS)
                    syslog.syslog(log_sys)

            if path == '/message':

                await message.message(websocket, data)

    finally:

        log_sys = "WEBSOCKET: {0}".format(websocket)
        syslog.syslog(log_sys)
        pass
        # USERS.remove(websocket)

MAIN = websockets.serve(app, "0.0.0.0", 6789)

asyncio.get_event_loop().run_until_complete(MAIN)
asyncio.get_event_loop().run_forever()
