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

    # log_sys = "USERS LIST HERE: {0}".format(users)
    # syslog.syslog(log_sys)

    for item in users.items():

        # log_sys = "{0} == {1}".format(item[0], system_id)
        # syslog.syslog(log_sys)

        if item[0] == system_id:

            # SEND UPDATE TO THE TAP
            system_info = COUCH_QUERY.get_by_id(system_id)
            system_info = revalidate_data(system_info)
            syslog.syslog("++++++++ UPDATE TAP SETTINGS ++++++++")
            syslog.syslog(json.dumps(system_info))
            syslog.syslog("======== UPDATE TAP SETTINGS ========")
            system_info['type'] = 'message'
            system_info['system_id'] = system_id
            system_info['msg_id'] = time.time()
            system_info['status'] = 'update'
            system_info = json.dumps(system_info)
            await asyncio.wait([item[1].send(system_info)])

            return 1

    # syslog.syslog("== UPDATEd ==")
    message = {}
    message['type'] = 'updated'
    message['time'] = time.time()
    message['status'] = 'ok'
    message = json.dumps(message)
    await asyncio.wait([websocket.send(message)])

    return 1

def reformat_units(value):
    """ REFORMAT """

    return float(value.split(" ")[0])


def revalidate_data(data):
    """ Validate Data"""

    tmp = {}
    if "soap_dose" in data:
        tmp['soap_dose'] = data['soap_dose']
        if not type(data['soap_dose']) in [int, float]:
            # if "milliliter" not in data['soap_dose']:
            tmp['soap_dose'] = reformat_units(data['soap_dose'])

    if "disinfect_dose" in data:
        tmp['disinfect_dose'] = data['disinfect_dose']
        if not type(data['disinfect_dose']) in [int, float]:
            # if "milliliter" not in data['disinfect_dose']:
            tmp['disinfect_dose'] = reformat_units(data['disinfect_dose'])

    if "init_wtr_temp" in data:

        tmp['init_wtr_temp'] = data['init_wtr_temp']
        if not type(data['init_wtr_temp']) == int:

            tmp['init_wtr_temp'] = reformat_units(data['init_wtr_temp'])

    if "wtr_shut_off_dly" in data:

        tmp['wtr_shut_off_dly'] = data['wtr_shut_off_dly']
        if not type(data['wtr_shut_off_dly']) == int:
            tmp['wtr_shut_off_dly'] = reformat_units(data['wtr_shut_off_dly'])

    if "wtr_temp_mem_tm" in data:

        tmp['wtr_temp_mem_tm'] = data['wtr_temp_mem_tm']
        if not type(data['wtr_temp_mem_tm']) == int:
            tmp['wtr_temp_mem_tm'] = reformat_units(data['wtr_temp_mem_tm'])

    if "bucket_mode_d" in data:

        tmp['bucket_mode_d'] = data['bucket_mode_d']
        if not type(data['bucket_mode_d']) in [int, float]:
            tmp['bucket_mode_d'] = reformat_units(data['bucket_mode_d'])

    if "tm_b4_stagn_flsh" in data:

        tmp['tm_b4_stagn_flsh'] = data['tm_b4_stagn_flsh']
        if not type(data['tm_b4_stagn_flsh']) == int:
            tmp['tm_b4_stagn_flsh'] =  reformat_units(data['tm_b4_stagn_flsh'])

    if "stagn_flsh_d" in data:

        tmp['stagn_flsh_d'] = data['stagn_flsh_d']
        if not type(data['stagn_flsh_d']) == int:
            # tmp['stagn_flsh_d'] =  reformat_units(data['stagn_flsh_d'])
            duration = data['stagn_flsh_d'].split(' ')[0]
            tmp['stagn_flsh_d'] =  int(duration.split(':')[0])

    if "stagn_flsh_u_dep" in data:

        tmp['stagn_flsh_u_dep'] = data['stagn_flsh_u_dep']
        if data['stagn_flsh_u_dep'] == "No":
            tmp['stagn_flsh_u_dep'] = 0

        if data['stagn_flsh_u_dep'] == "Yes":
            tmp['stagn_flsh_u_dep'] = 1

    if "thrm_flshng_tm" in data:

        tmp['thrm_flshng_tm'] = data['thrm_flshng_tm']
        if "At" in data['thrm_flshng_tm']:
            tmp['thrm_flshng_tm'] = tmp['thrm_flshng_tm'].split(" ")[1]

    if "thrm_flshng_day" in data:

        tmp['thrm_flshng_day'] = data['thrm_flshng_day']

        if data['thrm_flshng_day'] == "Off":
            tmp['thrm_flshng_day'] = 0

        if data['thrm_flshng_day'] == "Every Monday":
            tmp['thrm_flshng_day'] = 1

        if data['thrm_flshng_day'] == "Every Tuesday":
            tmp['thrm_flshng_day'] = 2

        if data['thrm_flshng_day'] == "Every Wednesday":
            tmp['thrm_flshng_day'] = 3

        if data['thrm_flshng_day'] == "Every Thursday":
            tmp['thrm_flshng_day'] = 4

        if data['thrm_flshng_day'] == "Every Friday":
            tmp['thrm_flshng_day'] = 5

        if data['thrm_flshng_day'] == "Every Saturday":
            tmp['thrm_flshng_day'] = 6

        if data['thrm_flshng_day'] == "Every Sunday":
            tmp['thrm_flshng_day'] = 7

        if data['thrm_flshng_day'] == "Every second Monday":
            tmp['thrm_flshng_day'] = 8

        if data['thrm_flshng_day'] == "Every second Tuesday":
            tmp['thrm_flshng_day'] = 9

        if data['thrm_flshng_day'] == "Every second Wednesday":
            tmp['thrm_flshng_day'] = 10

        if data['thrm_flshng_day'] == "Every second Thursday":
            tmp['thrm_flshng_day'] = 11

        if data['thrm_flshng_day'] == "Every second Friday":
            tmp['thrm_flshng_day'] = 12

        if data['thrm_flshng_day'] == "Every second Saturday":
            tmp['thrm_flshng_day'] = 13

        if data['thrm_flshng_day'] == "Every second Sunday":
            tmp['thrm_flshng_day'] = 14

        if data['thrm_flshng_day'] == "Every third Monday":
            tmp['thrm_flshng_day'] = 15

        if data['thrm_flshng_day'] == "Every third Tuesday":
            tmp['thrm_flshng_day'] = 16

        if data['thrm_flshng_day'] == "Every third Wednesday":
            tmp['thrm_flshng_day'] = 17

        if data['thrm_flshng_day'] == "Every third Thursday":
            tmp['thrm_flshng_day'] = 18

        if data['thrm_flshng_day'] == "Every third Friday":
            tmp['thrm_flshng_day'] = 19

        if data['thrm_flshng_day'] == "Every third Saturday":
            tmp['thrm_flshng_day'] = 20

        if data['thrm_flshng_day'] == "Every third Sunday":
            tmp['thrm_flshng_day'] = 21

        if data['thrm_flshng_day'] == "Coming Monday (single flush)":
            tmp['thrm_flshng_day'] = 22

        if data['thrm_flshng_day'] == "Coming Tuesday (single flush)":
            tmp['thrm_flshng_day'] = 23

        if data['thrm_flshng_day'] == "Coming Wednesday (single flush)":
            tmp['thrm_flshng_day'] = 24

        if data['thrm_flshng_day'] == "Coming Thursday (single flush)":
            tmp['thrm_flshng_day'] = 25

        if data['thrm_flshng_day'] == "Coming Friday (single flush)":
            tmp['thrm_flshng_day'] = 26

        if data['thrm_flshng_day'] == "Coming Saturday (single flush)":
            tmp['thrm_flshng_day'] = 27

        if data['thrm_flshng_day'] == "Coming Sunday (single flush)":
            tmp['thrm_flshng_day'] = 28

        if data['thrm_flshng_day'] == "Monthly every Monday":
            tmp['thrm_flshng_day'] = 29

        if data['thrm_flshng_day'] == "Monthly every Tuesday":
            tmp['thrm_flshng_day'] = 30

        if data['thrm_flshng_day'] == "Monthly every Wednesday":
            tmp['thrm_flshng_day'] = 31

        if data['thrm_flshng_day'] == "Monthly every Thursday":
            tmp['thrm_flshng_day'] = 32

        if data['thrm_flshng_day'] == "Monthly every Friday":
            tmp['thrm_flshng_day'] = 33

        if data['thrm_flshng_day'] == "Monthly every Saturday":
            tmp['thrm_flshng_day'] = 34

        if data['thrm_flshng_day'] == "Monthly every Sunday":
            tmp['thrm_flshng_day'] = 35

        if data['thrm_flshng_day'] == "Monday every 6 weeks":
            tmp['thrm_flshng_day'] = 36

        if data['thrm_flshng_day'] == "Tuesday every 6 weeks":
            tmp['thrm_flshng_day'] = 37

        if data['thrm_flshng_day'] == "Wednesday every 6 weeks":
            tmp['thrm_flshng_day'] = 38

        if data['thrm_flshng_day'] == "Thursday every 6 weeks":
            tmp['thrm_flshng_day'] = 39

        if data['thrm_flshng_day'] == "Friday every 6 weeks":
            tmp['thrm_flshng_day'] = 40

        if data['thrm_flshng_day'] == "Saturday every 6 weeks":
            tmp['thrm_flshng_day'] = 41

        if data['thrm_flshng_day'] == "Sunday every 6 weeks":
            tmp['thrm_flshng_day'] = 42

        if data['thrm_flshng_day'] == "Monday every 2 months":
            tmp['thrm_flshng_day'] = 43

        if data['thrm_flshng_day'] == "Tuesday every 2 months":
            tmp['thrm_flshng_day'] = 44

        if data['thrm_flshng_day'] == "Wednesday every 2 monthss":
            tmp['thrm_flshng_day'] = 45

        if data['thrm_flshng_day'] == "Thursday every 2 months":
            tmp['thrm_flshng_day'] = 46

        if data['thrm_flshng_day'] == "Friday every 2 months":
            tmp['thrm_flshng_day'] = 47

        if data['thrm_flshng_day'] == "Saturday every 2 months":
            tmp['thrm_flshng_day'] = 48

        if data['thrm_flshng_day'] == "Sunday every 2 months":
            tmp['thrm_flshng_day'] = 49

    if "thrm_flsh_temp" in data:

        tmp['thrm_flsh_temp'] =  data['thrm_flsh_temp']
        if not type(data['thrm_flsh_temp']) == int:
            tmp['thrm_flsh_temp'] = reformat_units(data['thrm_flsh_temp'])

    if "thrm_flsh_d" in data:

        tmp['thrm_flsh_d'] = data['thrm_flsh_d']
        if not type(data['thrm_flsh_d']) in [int, float]:

            # thrm_flsh_d = float(data['thrm_flsh_d'].split(" ")[0])
            duration = data['thrm_flsh_d'].split(" ")[0]
            mduration = duration.split(":")[0]
            sduration = duration.split(":")[1]
            total_duration int(mduration) * 60
            if int(sduration) > 0:
                total_duration += 30

            tmp['thrm_flsh_d'] = total_duration

    if "light_effect" in data:

        tmp['light_effect'] = data['light_effect']
        if data['light_effect'] == "Off":
            tmp['light_effect'] = 0

        if data['light_effect'] == "On":
            tmp['light_effect'] = 1

        if data['light_effect'] == "Pulse":
            tmp['light_effect'] = 2

    if "beep_tone" in data:

        tmp['beep_tone'] = data['beep_tone']
        if data['beep_tone'] == "Off":
            tmp['beep_tone'] = 0

        if not type(tmp['beep_tone']) == int:
            tmp['beep_tone'] = int(data['beep_tone'].split(" ")[1])

    if "clean_mode" in data:

        tmp['clean_mode'] = data['clean_mode']
        if data['clean_mode'] == "Off":
            tmp['clean_mode'] = 0

        if data['clean_mode'] == "ON":
            tmp['clean_mode'] = 1


    if "flow_heater_mode" in data:

        tmp['flow_heater_mode'] = data['flow_heater_mode']
        if data['flow_heater_mode'] == "Off":
            tmp['flow_heater_mode'] = 0

        if data['flow_heater_mode'] == "ON":
            tmp['flow_heater_mode'] = 1

    if "ir_range" in data:

        tmp['ir_range'] = data['ir_range']
        if not type(data['ir_range']) in [int, float]:
            tmp['ir_range'] = reformat_units(data['ir_range'])

    for key in tmp.keys():

        data[key] = tmp[key]

    return data
