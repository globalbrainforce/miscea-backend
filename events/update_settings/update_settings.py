""" UPDATE SETTINGS """
import json
import time
import asyncio
import syslog
from library.common import Common
from library.couch_queries import Queries
from library.sha_security import ShaSecurity
from library.postgresql_queries import PostgreSQL

COMMON = Common()
COUCH_QUERY = Queries()
SHASECURITY = ShaSecurity()
POSTGRES = PostgreSQL()

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

    log_sys = "USERS LIST HERE: {0}".format(users)
    syslog.syslog(log_sys)

    for item in users.items():

        log_sys = "{0} == {1}".format(item[0], system_id)
        syslog.syslog(log_sys)

        if not item[0] == system_id:

            # SEND UPDATE TO THE TAP
            system_info = COUCH_QUERY.get_by_id(system_id)
            system_info['type'] = 'message'
            system_info['system_id'] = system_id
            system_info['msg_id'] = time.time()
            system_info['status'] = 'update'
            system_info = json.dumps(system_info)
            await asyncio.wait([item[1].send(system_info)])

            return 1

    syslog.syslog("== UPDATEd ==")
    message = {}
    message['type'] = 'updated'
    message['time'] = time.time()
    message['status'] = 'ok'
    message = json.dumps(message)
    await asyncio.wait([websocket.send(message)])

    return 1
