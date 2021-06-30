""" APP """
import ssl
import socket
import time
import syslog
import asyncio
import json
import logging
import websockets

from events.auth import auth
from events.message import message
from events.update_settings import update_settings
from library.postgresql_queries import PostgreSQL
from library.couch_queries import Queries
from library.utils import Utils

logging.basicConfig()
CLIENTS = {}
POSTGRES = PostgreSQL()
UTILS = Utils()
COUCH_QUERY = Queries()

DATA_UPDATE = {}
DATA_UPDATE['state'] = False

CONDITIONS = []
CONDITIONS.append({
    "col": "state",
    "con": "=",
    "val": True}) 

POSTGRES.update('syst', DATA_UPDATE, CONDITIONS)

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
                    if data['type'] == 'settings':

                        system_id = data['system_id']

                        if not websocket_id in CLIENTS.keys():

                            CLIENTS[system_id] = websocket

                        data_update = {}
                        data_update['state'] = True

                        conditions = []
                        conditions.append({
                            "col": "syst_id",
                            "con": "=",
                            "val": system_id}) 

                        POSTGRES.update('syst', data_update, conditions)

                    if data['type'] == 'child_taps':

                        for online_tap in data['online_taps'] or []:

                            sql_str = " SELECT syst_id, need_to_update FROM syst where"
                            sql_str += " syst_id like 'system:{0}%'".format(online_tap[:12])
                            sql_str += " AND syst_id like '%{0}'".format(online_tap[-8:])
                            response = POSTGRES.query_fetch_one(sql_str)

                            if response:
                                tap_id = response['syst_id']

                                if not websocket_id in CLIENTS.keys():

                                    CLIENTS[tap_id] = websocket

                                data_update = {}
                                data_update['state'] = True

                                conditions = []
                                conditions.append({
                                    "col": "syst_id",
                                    "con": "=",
                                    "val": tap_id}) 

                                POSTGRES.update('syst', data_update, conditions)

                                # CHECK IF TAP SETTINGS NEEDS UPDATE
                                if response['need_to_update']:
                                    # msg_id = data['msg_id']
                                    system_info = COUCH_QUERY.get_by_id(tap_id)
                                    system_info = UTILS.revalidate_data(system_info)
                                    syslog.syslog("++++++++ UPDATE TAP SETTINGS ++++++++")
                                    syslog.syslog(json.dumps(system_info))
                                    syslog.syslog("======== UPDATE TAP SETTINGS ========")
                                    system_info['type'] = 'message'
                                    system_info['system_id'] = tap_id
                                    system_info['msg_id'] = time.time()
                                    system_info['status'] = 'update'
                                    system_info = json.dumps(system_info)
                                    await asyncio.wait([websocket.send(system_info)])

                                    data_update = {}
                                    data_update['need_to_update'] = False

                                    conditions = []
                                    conditions.append({
                                        "col": "syst_id",
                                        "con": "=",
                                        "val": tap_id}) 

                                    POSTGRES.update('syst', data_update, conditions)

                    if data['type'] == 'offline':

                        for offtap in data['offline_taps'] or []:


                            sql_str = "SELECT syst_id FROM syst where"
                            sql_str += " syst_id like 'system:{0}%'".format(offtap[:12])
                            sql_str += " AND syst_id like '%{0}'".format(offtap[-8:])
                            response = POSTGRES.query_fetch_one(sql_str)
                            if response:

                                new_users = {}

                                for item in CLIENTS.items():

                                    if not item[1] == websocket:

                                        new_users[item[0]] = item[1]

                                    else:

                                        data_update = {}
                                        data_update['state'] = False

                                        conditions = []
                                        conditions.append({
                                            "col": "syst_id",
                                            "con": "=",
                                            "val": response['syst_id']}) 

                                        POSTGRES.update('syst', data_update, conditions)

                                CLIENTS = new_users
                                log_sys = "New CLIENTS: {0}".format(CLIENTS)
                                syslog.syslog(log_sys)

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

                # GET SYSTEM TOKEN
                sql_str = "SELECT token FROM tap_accounts WHERE"
                sql_str += " system_id='{0}'".format(system_id)
                response = POSTGRES.query_fetch_one(sql_str)

                token = response['token']

                # GET SYSTEM IDS
                sql_str = "SELECT system_id FROM tap_accounts WHERE"
                sql_str += " token='{0}'".format(token)
                response = POSTGRES.query_fetch_all(sql_str)

                system_ids = [res['system_id'] for res in response or []]
                system_ids.append(system_id)

                data = {}
                data['state'] = False

                conditions = []
                conditions.append({
                    "col": "syst_id",
                    "con": "in",
                    "val": system_ids}) 

                POSTGRES.update('syst', data, conditions)

        CLIENTS = new_users
        log_sys = "New CLIENTS: {0}".format(CLIENTS)
        syslog.syslog(log_sys)


# hostname = 'websocket.miscea.com'
# # PROTOCOL_TLS_CLIENT requires valid cert chain and hostname
# context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
# context.load_verify_locations('/home/admin/cert/ssl-bundle.crt')

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
#     with context.wrap_socket(sock, server_hostname=hostname) as ssock:
#         print(ssock.version())


context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain('/home/admin/cert/miscea.com.crt', '/home/admin/cert/miscea.key')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    sock.bind(("0.0.0.0", 8443))
    sock.listen(5)
    with context.wrap_socket(sock, server_side=True) as ssock:
        conn, addr = ssock.accept()



# MAIN = websockets.serve(app, "0.0.0.0", 6789)

# asyncio.get_event_loop().run_until_complete(MAIN)
# asyncio.get_event_loop().run_forever()
