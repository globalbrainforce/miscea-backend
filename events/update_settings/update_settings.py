""" UPDATE SETTINGS """
import json
import time
import asyncio
import syslog
from library.common import Common
from library.sha_security import ShaSecurity
from library.postgresql_queries import PostgreSQL

COMMON = Common()
SHASECURITY = ShaSecurity()
POSTGRES = PostgreSQL()

async def update_settings(websocket, data, users):

    # if not 'token' in data.keys():

    #     syslog.syslog("NO TOKEN!")
    #     message = {}
    #     message['type'] = 'auth'
    #     message['status'] = 'Failed'
    #     message['alert'] = 'Invalid data!'
    #     message = json.dumps(message)
    #     await asyncio.wait([websocket.send(message)])

    #     return 0

    # VALIDATE TOKEN
    # CHECK IF TAP IS ONLINE
    # SEND UPDATE TO THE TAP

    syslog.syslog("== UPDATE ==")
    message = {}
    message['type'] = 'auth'
    message['time'] = time.time()
    message['status'] = 'ok'
    # message['new_token'] = new_token
    message = json.dumps(message)
    await asyncio.wait([websocket.send(message)])

    return 1

    # if COMMON.validate_default_token(data['token']):

    #     # default = data['system_data']
    #     default = data
    #     system_id = default['system_id']
    #     new_token = SHASECURITY.generate_token(False)

    #     tap_account = {}
    #     tap_account['system_id'] = system_id
    #     tap_account['token'] = new_token
    #     tap_account['last_login'] = time.time()

    #     sql_str = "SELECT tap_account_id FROM tap_accounts WHERE"
    #     sql_str += " system_id='{0}'".format(system_id)
    #     response = POSTGRES.query_fetch_one(sql_str)

    #     if response:

    #         # INIT CONDITION
    #         conditions = []

    #         # CONDITION FOR QUERY
    #         conditions.append({
    #             "col": "tap_account_id",
    #             "con": "=",
    #             "val": response['tap_account_id']
    #             })

    #         # UPDATE TAP ACCOUNT TOKEN
    #         tap_account['update_on'] = time.time()

    #         POSTGRES.update('tap_accounts', tap_account, conditions)

    #     else:

    #         # INSERT TAP ACCOUNT TOKEN
    #         tap_account['tap_account_id'] = SHASECURITY.generate_token(False)
    #         tap_account['created_on'] = time.time()

    #         POSTGRES.insert('tap_accounts', tap_account)

    #     syslog.syslog("VALID TOKEN!")
    #     message = {}
    #     message['type'] = 'auth'
    #     message['time'] = time.time()
    #     message['status'] = 'ok'
    #     message['new_token'] = new_token
    #     message = json.dumps(message)
    #     await asyncio.wait([websocket.send(message)])

    #     return 1

    # else:

    #     syslog.syslog("INVALID TOKEN!")
    #     message = {}
    #     message['type'] = 'auth'
    #     message['status'] = 'Failed'
    #     message['alert'] = 'Invalid data!'
    #     message = json.dumps(message)
    #     await asyncio.wait([websocket.send(message)])

    #     return 0
