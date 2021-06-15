""" APP """
import syslog
import asyncio
import json
import logging
import websockets

from events.auth import auth
from events.message import message
from events.update_settings import update_settings
from library.postgresql_queries import PostgreSQL

logging.basicConfig()
CLIENTS = {}
POSTGRES = PostgreSQL()

async def app(websocket, path):
    """ MAIN APPLICATION """

    global CLIENTS

    try:

        # state_val = {}
        # state_val['type'] = "state"
        # state_val['value'] = 1

        # await websocket.send(state_val)
        async for webs in websocket:

            data = json.loads(webs)

            if path == '/auth':

                await auth.auth(websocket, data)

            if path == '/message':

                if await message.message(websocket, data):

                    websocket_id = data['system_id']

                    if not websocket_id in CLIENTS.keys():

                        CLIENTS[websocket_id] = websocket

                    # log_sys = "CLIENTS: {0}".format(CLIENTS)
                    # syslog.syslog(log_sys)

            if path == '/update-settings':

                # log_sys = "BEFORE CLIENTS: {0}".format(CLIENTS)
                # syslog.syslog(log_sys)
                await update_settings.update_settings(websocket, data, CLIENTS)

    except:

        print("may error!")
        raise

    finally:

        new_users = {}

        for item in CLIENTS.items():

            if not item[1] == websocket:

                new_users[item[0]] = item[1]

            else:

                system_id = item[0]
                data = {}
                data['state'] = False

                conditions = []
                conditions.append({
                    "col": "syst_id",
                    "con": "=",
                    "val": system_id}) 

                POSTGRES.update('syst', data, conditions, log=True)

        CLIENTS = new_users
        log_sys = "New CLIENTS: {0}".format(CLIENTS)
        syslog.syslog(log_sys)

MAIN = websockets.serve(app, "0.0.0.0", 6789)

asyncio.get_event_loop().run_until_complete(MAIN)
asyncio.get_event_loop().run_forever()
