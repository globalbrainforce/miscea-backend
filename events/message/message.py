""" MESSAGE """
import json
import time
import asyncio
import requests

from library.sha_security import ShaSecurity
from library.couch_database import CouchDatabase
from library.couch_queries import Queries

SHA_SECURITY = ShaSecurity()
COUCHDB = CouchDatabase()
COUCH_QUERY = Queries()
ESTABLISHMENT = 'establishment:381741ac4b5f4a4785ffdf2e025975fc'

async def message(websocket, data):

    if not 'token' in data.keys():

        message = {}
        message['type'] = 'message'
        message['status'] = 'Failed'
        message['alert'] = 'Invalid data!'
        message = json.dumps(message)
        await asyncio.wait([websocket.send(message)])

        return 0

    if data['token'] == '300c2c3706886d94aeefd6e7f7130ab08346590533d4c5b24ccaea9baa5211ed':
        mtype = 'message'

        if data['type'] == 'settings':
            mtype = 'settings'
            check_settings(data)

        elif data['type'] =='soap-activity':
            # SOAP ACTIVITY

            mtype = 'soap-activity'

            sda = {}
            sda['_id'] = 'data#sa:' + str(SHA_SECURITY.generate_token(False))
            sda['timestamp'] = data['timestamp']
            sda['liquid_1_level'] = data['liquid_1_level']
            sda['liquid_1_dose'] = data['liquid_1_dose']
            sda['type'] = 'data'
            sda['system_id'] = data['system_id']
            sda['establishment_id'] = ESTABLISHMENT

            couch_url = COUCHDB.couch_db_link()
            headers = {"Content-Type" : "application/json"}
            response = requests.post(couch_url, data=json.dumps(sda), headers=headers)

            json_data = response.json()

        elif data['type'] == 'disinfectant-activity':
            # DISINFECTANT
            
            sda = {}
            sda['_id'] = 'data#da:' + str(SHA_SECURITY.generate_token(False))
            sda['timestamp'] = data['timestamp']
            sda['liquid_2_level'] = data['liquid_2_level']
            sda['liquid_2_dose'] = data['liquid_2_dose']
            sda['type'] = 'data'
            sda['system_id'] = data['system_id']
            sda['establishment_id'] = ESTABLISHMENT

            couch_url = COUCHDB.couch_db_link()
            headers = {"Content-Type" : "application/json"}
            response = requests.post(couch_url, data=json.dumps(sda), headers=headers)

            json_data = response.json()

        elif data['type'] =='water-activity':
            # WATER ACTIVITY

            wactvt = {}
            wactvt['_id'] = 'data#wa:' + str(SHA_SECURITY.generate_token(False))
            wactvt['timestamp'] = data['timestamp']
            wactvt['reason'] = data['reason']
            wactvt['duration'] = data['duration']
            wactvt['temperature'] = data['temperature']
            wactvt['flow_output'] = data['flow_output']
            wactvt['type'] = 'data'
            wactvt['system_id'] = data['system_id']
            wactvt['establishment_id'] = ESTABLISHMENT

            couch_url = COUCHDB.couch_db_link()
            headers = {"Content-Type" : "application/json"}
            response = requests.post(couch_url, data=json.dumps(sda), headers=headers)

            json_data = response.json()

        message = {}
        message['type'] = mtype
        message['status'] = 'ok'
        message = json.dumps(message)
        await asyncio.wait([websocket.send(message)])

        return 1

    else:

        message = {}
        message['type'] = 'message'
        message['status'] = 'Failed'
        message['alert'] = 'Invalid data!'
        message = json.dumps(message)
        await asyncio.wait([websocket.send(message)])

        return 0

def check_settings(data):

    default = data['system_data']
    system_id = default['system_id']

    doc = COUCH_QUERY.get_by_id(system_id)

    # CHECK IF SYSTEM ID EXIST
    # IF NOT
    if 'error' in doc.keys():

        # ADD AS NEW TOP
        current = time.time()
        system = {}
        system['_id'] = system_id
        system['article_number'] = default['article_number']
        system['update_on'] = current
        system['created_on'] = current
        system['serial'] = str(SHA_SECURITY.generate_token(False))[:10]
        system['model'] = ""
        system['description'] = ""
        system['soap_dose'] = default['soap_dose']
        system['disinfect_dose'] = default['disinfect_dose']
        system['init_wtr_temp'] = default['init_wtr_temp']
        system['wtr_shut_off_dly'] = default['wtr_shut_off_dly']
        system['wtr_temp_mem_tm'] = default['wtr_temp_mem_tm']
        system['bucket_mode_d'] = default['bucket_mode_d']
        system['tm_b4_stagn_flsh'] = default['tm_b4_stagn_flsh']
        system['stagn_flsh_d'] = default['stagn_flsh_d']
        system['stagn_flsh_u_dep'] = default['stagn_flsh_u_dep']
        system['thrm_flshng_tm'] = default['thrm_flshng_tm']
        system['thrm_flshng_day'] = default['thrm_flshng_day']
        system['thrm_flsh_temp'] = default['thrm_flsh_temp']
        system['thrm_flsh_d'] = default['thrm_flsh_d']
        system['light_effect'] = default['light_effect']
        system['beep_tone'] = default['beep_tone']
        system['clean_mode'] = default['clean_mode']
        system['flow_heater_mode'] = default['flow_heater_mode']
        system['ir_range'] = default['ir_range']
        system['type'] = "systems_list"
        system['establishment_id'] = ESTABLISHMENT

    # ELSE
    else:

        pass
        # RETURN SYSTEM ID
