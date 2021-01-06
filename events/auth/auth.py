""" AUTH """
import json
import time
import asyncio

from library.sha_security import ShaSecurity
from library.couch_queries import Queries

SHA_SECURITY = ShaSecurity()
COUCH_QUERY = Queries()

async def auth(websocket, data):

    if not 'token' in data.keys():

        message = {}
        message['type'] = 'auth'
        message['status'] = 'Failed'
        message['alert'] = 'Invalid data!'
        message = json.dumps(message)
        await asyncio.wait([websocket.send(message)])

        return 0

    if data['token'] == '269c2c3706886d94aeefd6e7f7130ab08346590533d4c5b24ccaea9baa5211ec':

        system_id = 'system:' + '43876adc83a24d6191c2edd4158de874'
        doc = COUCH_QUERY.get_by_id(system_id)
        print("system: ", doc)
        establishment = "establishment:381741ac4b5f4a4785ffdf2e025975fc"
        # CHECK IF SYSTEM ID EXIST
        # IF NOT
            # ADD AS NEW TOP
            # RETURN SYSTEM ID
        # ELSE
            # RETURN SYSTEM ID

        # current = time.time()
        # system = {}
        # system['_id'] = system_id
        # system['article_number'] = 'CER2S1NCDE'
        # system['update_on'] = current
        # system['created_on'] = current
        # system['serial'] = str(SHA_SECURITY.generate_token(False))[:10]
        # system['model'] = ""
        # system['description'] = ""
        # system['soap_dose'] = default['soap_dose']
        # system['disinfect_dose'] = default['disinfect_dose']
        # system['init_wtr_temp'] = default['init_wtr_temp']
        # system['wtr_shut_off_dly'] = default['wtr_shut_off_dly']
        # system['wtr_temp_mem_tm'] = default['wtr_temp_mem_tm']
        # system['bucket_mode_d'] = default['bucket_mode_d']
        # system['tm_b4_stagn_flsh'] = default['tm_b4_stagn_flsh']
        # system['stagn_flsh_d'] = default['stagn_flsh_d']
        # system['stagn_flsh_u_dep'] = default['stagn_flsh_u_dep']
        # system['thrm_flshng_tm'] = default['thrm_flshng_tm']
        # system['thrm_flshng_day'] = default['thrm_flshng_day']
        # system['thrm_flsh_temp'] = default['thrm_flsh_temp']
        # system['thrm_flsh_d'] = default['thrm_flsh_d']
        # system['light_effect'] = default['light_effect']
        # system['beep_tone'] = default['beep_tone']
        # system['clean_mode'] = default['clean_mode']
        # system['flow_heater_mode'] = default['flow_heater_mode']
        # system['ir_range'] = default['ir_range']
        # system['type'] = "systems_list"
        # system['establishment_id'] = establishment


        message = {}
        message['type'] = 'auth'
        message['time'] = time.time()
        message['doc'] = doc
        message['status'] = 'ok'
        message['new_token'] = '300c2c3706886d94aeefd6e7f7130ab08346590533d4c5b24ccaea9baa5211ed'
        message = json.dumps(message)
        await asyncio.wait([websocket.send(message)])

        return 1

    else:

        message = {}
        message['type'] = 'auth'
        message['status'] = 'Failed'
        message['alert'] = 'Invalid data!'
        message = json.dumps(message)
        await asyncio.wait([websocket.send(message)])

        return 0








# from flask import request
# from library.common import Common
# from flask_socketio import SocketIO, emit
# from library.utils import Utils

# try:

#     from __main__ import SOCKETIO

# except ImportError:

#     from app import SOCKETIO

# utils = Utils()

# @SOCKETIO.on('auth')
# def auth(json):
#     """ authentication """

#     clients = []
#     clients.append(request.sid)

#     utils.data_log(divider=True)
#     utils.data_log('Auth recived: {0}'.format(json))
#     utils.data_log(divider=True)

#     if not 'token' in json.keys():

#         response = {}
#         response['status'] = 'Failed'
#         response['alert'] = 'Invalid data!'
#         emit('my response', response, room=clients[0])

#     if json['token'] == '269c2c3706886d94aeefd6e7f7130ab08346590533d4c5b24ccaea9baa5211ec':

#         response = {}
#         response['status'] = 'ok'
#         response['new_token'] = '300c2c3706886d94aeefd6e7f7130ab08346590533d4c5b24ccaea9baa5211ed'
#         emit('my response', response, room=clients[0])
