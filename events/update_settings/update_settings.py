""" UPDATE SETTINGS """
import syslog
import json
import time
import asyncio
import syslog
from library.common import Common
from library.couch_queries import Queries
from library.sha_security import ShaSecurity
from library.postgresql_queries import PostgreSQL
from library.utils import Utils

COMMON = Common()
COUCH_QUERY = Queries()
SHASECURITY = ShaSecurity()
POSTGRES = PostgreSQL()
UTILS = Utils()

async def update_settings(websocket, data, users):

    # CHECK TOKEN EXIST
    if not 'token' in data.keys() or not 'system_id' in data.keys():

        syslog.syslog("NO TOKEN!")
        message = {}
        message['type'] = 'auth'
        message['status'] = 'Failed'
        message['alert'] = 'Invalid data!'
        message = json.dumps(message)
        await asyncio.wait([websocket.send(message)])

        return 0

    # VALIDATE TOKEN
    sql_str = "SELECT token_id FROM default_tokens WHERE"
    sql_str += " token='{0}'".format(data['token'])

    if not POSTGRES.query_fetch_one(sql_str):

        syslog.syslog("NO TOKEN!")
        message = {}
        message['type'] = 'auth'
        message['status'] = 'Failed'
        message['alert'] = 'Invalid data!'
        message = json.dumps(message)
        await asyncio.wait([websocket.send(message)])

        return 0

    # CHECK IF TAP IS ONLINE
    system_id = data['system_id']

    for item in users.items():

        if item[0] == system_id:

            # SEND UPDATE TO THE TAP
            system_info = COUCH_QUERY.get_by_id(system_id)
            system_info = UTILS.revalidate_data(system_info)
            syslog.syslog("++++++++ UPDATE TAP SETTINGS ++++++++")
            syslog.syslog(json.dumps(system_info))
            syslog.syslog("======== UPDATE TAP SETTINGS ========")
            system_info['type'] = 'message'
            system_info['system_id'] = system_id
            system_info['msg_id'] = time.time()
            system_info['status'] = 'update'
            system_info = json.dumps(system_info)
            await asyncio.wait([item[1].send(system_info)])

            data_update = {}
            data_update['need_to_update'] = False

            conditions = []
            conditions.append({
                "col": "syst_id",
                "con": "=",
                "val": system_id}) 

            POSTGRES.update('syst', data_update, conditions)

            return 1

    message = {}
    message['type'] = 'updated'
    message['time'] = time.time()
    message['status'] = 'ok'
    message = json.dumps(message)
    await asyncio.wait([websocket.send(message)])

    return 1
