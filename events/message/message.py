""" MESSAGE """
import json
import time
import asyncio
import requests
import syslog

from library.common import Common
from library.couch_queries import Queries
from library.sha_security import ShaSecurity
from library.couch_database import CouchDatabase
from library.postgresql_queries import PostgreSQL

COMMON = Common()
COUCH_QUERY = Queries()
POSTGRES = PostgreSQL()
COUCHDB = CouchDatabase()
SHA_SECURITY = ShaSecurity()
ESTABLISHMENT = 'establishment:381741ac4b5f4a4785ffdf2e025975fc'

SYSTEM_KEYS = [
    'article_number',
    'soap_dose',
    'disinfect_dose',
    'init_wtr_temp',
    'wtr_shut_off_dly',
    'wtr_temp_mem_tm',
    'bucket_mode_d',
    'tm_b4_stagn_flsh',
    'stagn_flsh_d',
    'stagn_flsh_u_dep',
    'thrm_flshng_tm',
    'thrm_flshng_day',
    'thrm_flsh_temp',
    'thrm_flsh_d',
    'light_effect',
    'beep_tone',
    'clean_mode',
    'flow_heater_mode',
    'ir_range',
    'description'
]

async def message(websocket, data):

    # system_id = ""

    # if data['type'] == 'settings':

    #     # default = data['system_data']
    #     default = data
    #     system_id = default['system_id']

    # else:

    #     # default = data['activity']
    #     default = data
    #     system_id = default['system_id']

    default = data
    system_id = default['system_id']
    msg_id = default['msg_id']

    if not 'token' in data.keys():

        message = {}
        message['type'] = 'message'
        message['status'] = 'Failed'
        message['system_id'] = system_id
        message['alert'] = 'Invalid data!'
        message = json.dumps(message)
        await asyncio.wait([websocket.send(message)])

        return 0

    if COMMON.validate_tap_token(data['token'], system_id):

        mtype = 'message'

        if data['type'] == 'settings':
            mtype = 'settings'
            system_info = check_settings(data)

            if system_info:

                system_info['type'] = mtype
                system_info['system_id'] = system_id
                system_info['msg_id'] = msg_id
                system_info['status'] = 'update'
                system_info = json.dumps(system_info)
                await asyncio.wait([websocket.send(system_info)])

                return 1

        elif data['type'] =='soap-activity':
            # SOAP ACTIVITY

            mtype = 'soap-activity'
            # activity = data['activity']
            activity = data

            sda = {}
            sda['_id'] = 'data#sa:' + str(SHA_SECURITY.generate_token(False))
            sda['timestamp'] = activity['timestamp']
            sda['liquid_1_level'] = activity['liquid_1_level']
            sda['liquid_1_dose'] = activity['liquid_1_dose']
            sda['type'] = 'data'
            sda['system_id'] = activity['system_id']
            sda['establishment_id'] = ESTABLISHMENT

            couch_url = COUCHDB.couch_db_link()
            headers = {"Content-Type" : "application/json"}
            response = requests.post(couch_url, data=json.dumps(sda), headers=headers)

            syslog.syslog("++++++++ SOAP ++++++++")
            syslog.syslog(json.dumps(sda))
            syslog.syslog("======== SOAP ========")

            response.json()

            # RUN REPORTS FOR SOAP ACTIVITIES
            reports(ESTABLISHMENT, system_id, 'data%23sa', sda)

        elif data['type'] == 'disinfectant-activity':
            # DISINFECTANT

            mtype = 'disinfectant-activity'
            # activity = data['activity']
            activity = data

            sda = {}
            sda['_id'] = 'data#da:' + str(SHA_SECURITY.generate_token(False))
            sda['timestamp'] = activity['timestamp']
            sda['liquid_2_level'] = activity['liquid_2_level']
            sda['liquid_2_dose'] = activity['liquid_2_dose']
            sda['type'] = 'data'
            sda['system_id'] = activity['system_id']
            sda['establishment_id'] = ESTABLISHMENT

            syslog.syslog("++++++++ DISINFECTANT ++++++++")
            syslog.syslog(json.dumps(sda))
            syslog.syslog("======== DISINFECTANT ========")

            couch_url = COUCHDB.couch_db_link()
            headers = {"Content-Type" : "application/json"}
            response = requests.post(couch_url, data=json.dumps(sda), headers=headers)

            response.json()

            # RUN REPORTS FOR DISINFECTANT ACTIVITIES
            reports(ESTABLISHMENT, system_id, 'data%23da', sda)

        elif data['type'] =='water-activity':
            # WATER ACTIVITY

            mtype = 'water-activity'
            # activity = data['activity']
            activity = data
            system_id = activity['system_id']
            water_data_id = 'data#wa:' + str(SHA_SECURITY.generate_token(False))

            wactvt = {}
            wactvt['_id'] = water_data_id
            wactvt['timestamp'] = activity['timestamp']
            wactvt['reason'] = activity['reason']
            wactvt['duration'] = activity['duration']
            wactvt['temperature'] = activity['temperature']
            wactvt['flow_output'] = activity['flow_output']
            wactvt['type'] = 'data'
            wactvt['system_id'] = system_id
            wactvt['establishment_id'] = ESTABLISHMENT

            syslog.syslog("++++++++ WATER ++++++++")
            syslog.syslog(json.dumps(wactvt))
            syslog.syslog("======== WATER ========")

            # SAVE WATER ACTIVITY
            data_wact = {}
            data_wact['water_activity_id'] = wactvt['_id']
            data_wact['establ_id'] = ESTABLISHMENT
            data_wact['syst_id'] = system_id
            data_wact['timestamp'] = wactvt['timestamp']
            data_wact['reason'] = wactvt['reason']
            data_wact['duration'] = wactvt['duration']
            data_wact['temperature'] = wactvt['temperature']

            epoch = COMMON.get_epoch_date_hour(data_wact['timestamp'])
            data_wact['time'] = epoch['time']
            data_wact['date'] = epoch['date'].replace('/', '.')

            degree_sign = u"\N{DEGREE SIGN}"
            degree = "{0}C".format(degree_sign)
            data_wact['temperature'] = data_wact['temperature'].replace(" Degrees Celsius", degree)

            # FORMAT DURATION OF THERMAL DISINFECTION
            if data_wact['reason'] == "Thermal disinfection":

                duration = data_wact['duration'].split(" ")
                period = duration[-1]
                interval = duration[0].split(".")

                minutes = interval[0]
                if len(interval[0]) == 1:
                    minutes = "0{0}".format(interval[0])

                seconds = ""
                if int(interval[-1]) > 0:

                    seconds = ":{0}".format(interval[-1])
                    if len(interval[-1]) == 1:
                        seconds = ":0{0}".format(interval[-1])

                data_wact['duration'] = "00:{0}{1} {2}".format(minutes, seconds, period)

            if data_wact['reason'] == "Flush":

                data_wact['reason'] = "Stagnation Flush"

            data_wact['flow_output'] = wactvt['flow_output']
            data_wact['created_on'] = wactvt['timestamp']
            POSTGRES.insert('water_activities', data_wact)

            couch_url = COUCHDB.couch_db_link()
            headers = {"Content-Type" : "application/json"}
            requests.post(couch_url, data=json.dumps(wactvt), headers=headers)

            # RUN REPORTS FOR WATER ACTIVITIES
            reports(ESTABLISHMENT, system_id, 'data%23wa', wactvt)

            # SAVE LATEST ACTIVITIES
            latest_activities(ESTABLISHMENT, system_id, 'data%23wa')

        message = {}
        message['type'] = mtype
        message['system_id'] = system_id
        message['msg_id'] = msg_id
        message['status'] = 'ok'
        message = json.dumps(message)
        await asyncio.wait([websocket.send(message)])

        return 1

    else:

        message = {}
        message['type'] = 'message'
        message['system_id'] = system_id
        message['msg_id'] = msg_id
        message['status'] = 'Failed'
        message['alert'] = 'Invalid data!'
        message = json.dumps(message)
        await asyncio.wait([websocket.send(message)])

        return 0

def check_settings(data):

    # default = data['system_data']
    default = data
    system_id = default['system_id']

    system_info = COUCH_QUERY.get_by_id(system_id)

    syslog.syslog("++++++++ SETTINGS ++++++++")
    syslog.syslog(json.dumps(system_info))
    syslog.syslog("======== SETTINGS ========")

    # CHECK IF SYSTEM ID EXIST
    # IF NOT
    if 'error' in system_info.keys():

        # GET DEFAULT NETWORK ID
        network_id = ""

        if 'network_id' in default.keys():

            if not default['network_id']:

                network_id = get_default_network()

            else:

                # VALIDATE NETWORK ID
                sql_str = "SELECT * FROM network WHERE"
                sql_str += " network_id='{0}'".format(default['network_id'])

                if POSTGRES.query_fetch_one(sql_str):

                    network_id = default['network_id']

                else:

                    network_id = get_default_network()

        else:

            network_id = get_default_network()

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

        if 'description' in default.keys():

            system['description'] = default['description']

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

        syslog.syslog("++++++++ CREATE SETTINGS ++++++++")
        syslog.syslog(json.dumps(system))
        syslog.syslog("======== CREATE SETTINGS ========")

        # INSERT TAP DATA ON COUCHDB
        couch_url = COUCHDB.couch_db_link()
        headers = {"Content-Type" : "application/json"}
        requests.post(couch_url, data=json.dumps(system), headers=headers)

        # INSERT TAP DATA ON POSTGRESQL
        syst_data = {}
        syst_data['syst_id'] = system_id
        syst_data['establ_id'] = ESTABLISHMENT
        syst_data['network_id'] = network_id
        syst_data['article_number'] = system['article_number']
        syst_data['description'] = system['description']
        syst_data['update_on'] = time.time()
        syst_data['created_on'] = time.time()

        POSTGRES.insert('syst', data)
        
        # ADD TAP ON ACCOUNTS
        sql_str = "SELECT account_id FROM account_network WHERE"
        sql_str += " network_id='{0}'".format(network_id)
        account_ids = POSTGRES.query_fetch_all(sql_str)
        
        for account_id in account_ids or []:

            # GET ACCOUNT DEFAULT GROUP
            # BIND TAP TO ACCOUNT DEFAULT GROUP
            # new_syst = {}
            # new_syst['syst_id'] = system_id
            # new_syst['group_id'] = "411a6b596cdd485e85fdb825ebf0167a"

            # self.postgres.insert('grp_syst', new_syst)

            pass

            # BIND TAP TO ACCOUNT
            # account_syst

        return 0

    else:

        is_update = False
        # CHECK UPDATE
        for system_key in SYSTEM_KEYS:

            if not default[system_key] == system_info[system_key]:

                is_update = True

        if is_update:

            # SERVER NEED TO UPDATE TOP CODE HERE
            if not default['description'] == system_info['description']:

                system_info['description'] = default['description']
                COUCH_QUERY.update(system_info, system_id)

                data = {}
                data['description'] = default['description']
                conditions = []
                conditions.append({
                    "col": "syst_id",
                    "con": "=",
                    "val": system_id})  

                POSTGRES.update('syst', data, conditions)

            return 0

        return 0


def reports(estab_id, system_id, partition, activity_data=None):
    """ Reports """

    current_date = epoch_day(time.time())

    epoch_time = days_update(current_date)
    epoch_time -= 1

    # GET LAST DAY UPDATE
    timestamp = get_next_timestamp(estab_id, system_id, partition)

    if not timestamp:

        return 0

    late_et = days_update(timestamp, 1, True)
    late_st = days_update(late_et, 1)

    new_et = late_et

    if int(new_et) == 0 and int(epoch_time) -1 and activity_data:

        results = get_calculation(partition, activity_data, estab_id, system_id)

        update_results(estab_id, system_id, partition, current_date, results)

    # EACH DAYS
    while int(new_et) <= int(epoch_time):

        late_et = days_update(late_et, 1, True)
        late_st = days_update(late_et, 1)

        if late_st > epoch_time:

            break

        new_et = late_et - 1

        # GET DATAS
        values = get_all_data(estab_id, system_id, partition, late_st, new_et)

        if values:

            # CALCULATE
            results = calculate_values(values, partition)

            # SAVE RESULTS
            if not save_results(estab_id, system_id, partition, late_st, results):
                return 0

def latest_activities(estab_id, system_id, partition):
    """ SAVE LATEST ACTIVITIES """

    values = COUCH_QUERY.latest_datas(
        estab_id,
        system_id,
        partition,
        limit=20,
        descending=False
    )

    if not values:

        return 1

    values = sorted(values, key=lambda i: i["timestamp"], reverse=True)

    val1 = values[0]

    sql_str = "SELECT date_of_data FROM latest_activities WHERE"
    sql_str += " syst_id='{0}'".format(system_id)
    sql_str += " ORDER BY date_of_data DESC LIMIT 1"

    epoch_date = POSTGRES.query_fetch_one(sql_str)

    if epoch_date:

        if epoch_date['date_of_data'] == int(val1['timestamp']):

            return 1

        else:

            conditions = []

            conditions.append({
                "col": "syst_id",
                "con": "=",
                "val": system_id
                })

            POSTGRES.delete('latest_activities', conditions)

    for value in values:

        timestamp = time.time()
        wdata = {}
        wdata['latest_activity_id'] = value['_id']
        wdata['establ_id'] = value['establishment_id']
        wdata['syst_id'] = value['system_id']
        wdata['duration'] = value['duration']
        wdata['temperature'] = value['temperature']
        wdata['type'] = value['type']
        wdata['reason'] = value['reason']
        wdata['flow_output'] = value['flow_output']
        wdata['date_of_data'] = int(value['timestamp'])
        wdata['update_on'] = timestamp
        wdata['created_on'] = timestamp

        # SAVE
        POSTGRES.insert('latest_activities', wdata, 'latest_activity_id')

    return 1

def get_next_timestamp(estab_id, system_id, partition):
    """ GET FIRST TIMESTAMP """

    sql_str = ""
    if partition == 'data%23sa':

        sql_str = "SELECT date_of_data FROM liquid_1_activities WHERE"

    elif partition == 'data%23da':

        sql_str = "SELECT date_of_data FROM liquid_2_activities WHERE"

    else:

        sql_str = "SELECT date_of_data FROM w_activities WHERE"

    sql_str += " establ_id='{0}'".format(estab_id)
    sql_str += " AND syst_id='{0}'".format(system_id)
    sql_str += " ORDER BY date_of_data DESC LIMIT 1"

    epoch_date = POSTGRES.query_fetch_one(sql_str)

    timestamp = 0
    if epoch_date:

        timestamp = epoch_date['date_of_data']

    else:

        values = COUCH_QUERY.get_complete_values(
            estab_id,
            system_id,
            partition,
            start=str(9999999999),
            end=str(26763),
            flag='one_doc',
            descending=False
        )

        if not values:

            return 0

        timestamp = values['timestamp']
        timestamp = days_update(timestamp, 1, False)

    return timestamp

def epoch_day(timestamp):
    """ Epoch Day """
    try:

        named_tuple = time.localtime(int(timestamp))

        # GET YEAR MONTH DAY
        year = int(time.strftime("%Y", named_tuple))
        month = int(time.strftime("%m", named_tuple))
        day = int(time.strftime("%d", named_tuple))

        # Date in tuple
        date_tuple = (year, month, day, 0, 0, 0, 0, 0, 0)

        return time.mktime(date_tuple)

    except:

        return 0

def get_all_data(estab_id, system_id, partition, start_time, end_time):
    """ Return all data """

    values = COUCH_QUERY.get_complete_values(
        estab_id,
        system_id,
        partition,
        start=start_time,
        end=end_time,
        flag='all'
    )

    return values

def calculate_values(values, partition):
    """ Calculate Values """

    results = {}

    if partition == 'data%23wa':

        flow_output = 0
        # EACH VALUES
        for value in values:

            flow_output += float_data(value['flow_output'].split("L")[0])

            if value['reason'].upper() == 'FLUSH':

                timestamp = time.time()
                wdata = {}
                wdata['wf_activity_id'] = value['_id']
                wdata['establ_id'] = value['establishment_id']
                wdata['syst_id'] = value['system_id']
                wdata['duration'] = value['duration']
                wdata['temperature'] = value['temperature']
                wdata['type'] = value['type']
                wdata['reason'] = value['reason']
                wdata['flow_output'] = value['flow_output']
                wdata['date_of_data'] = int(value['timestamp'])
                wdata['update_on'] = timestamp
                wdata['created_on'] = timestamp

                # SAVE
                POSTGRES.insert('wf_activities', wdata, 'wf_activity_id')

            elif value['reason'].upper() == 'THERMAL DISINFECTION':

                timestamp = time.time()
                wdata = {}
                wdata['wt_activity_id'] = value['_id']
                wdata['establ_id'] = value['establishment_id']
                wdata['syst_id'] = value['system_id']
                wdata['duration'] = value['duration']
                wdata['temperature'] = value['temperature']
                wdata['type'] = value['type']
                wdata['reason'] = value['reason']
                wdata['flow_output'] = value['flow_output']
                wdata['date_of_data'] = int(value['timestamp'])
                wdata['update_on'] = timestamp
                wdata['created_on'] = timestamp

                # SAVE
                POSTGRES.insert('wt_activities', wdata, 'wt_activity_id')

        results['flow_output'] = flow_output

    elif partition == 'data%23sa':

        liquid1 = 0
        # EACH VALUES
        for value in values:

            if value:

                try:

                    liquid1 += float_data(value['liquid_1_dose'])

                except:

                    pass

                try:

                    liquid1 += float_data(value['liquid_1_dose'])

                except:

                    pass

        results['liquid1'] = liquid1

    elif partition == 'data%23da':

        liquid2 = 0
        # EACH VALUES
        for value in values:

            if value:

                try:

                    liquid2 += float_data(value['liquid_2_dose'])

                except:

                    pass

                try:

                    liquid2 += float_data(value['liquid_2_dose'])

                except:

                    pass

        results['liquid2'] = liquid2

    else:

        print("Invalid partition: ", partition)

    return results

def float_data(data):
    """ Return Float Data """

    try:

        return float(data)

    except:

        return 0

def save_results(estab_id, system_id, partition, timestamp, results):
    """ SAVE RESULTS """

    data = {}
    current_time = time.time()

    if partition == 'data%23wa':

        data['w_activity_id'] = SHA_SECURITY.generate_token(False)
        data['establ_id'] = estab_id
        data['syst_id'] = system_id
        data['results'] = json.dumps(results)
        data['date_of_data'] = timestamp
        data['update_on'] = current_time
        data['created_on'] = current_time
        if POSTGRES.insert('w_activities', data, 'w_activity_id'):

            return 1

    elif partition == 'data%23sa':

        data['liquid_1_activity_id'] = SHA_SECURITY.generate_token(False)
        data['establ_id'] = estab_id
        data['syst_id'] = system_id
        data['results'] = json.dumps(results)
        data['date_of_data'] = timestamp
        data['update_on'] = current_time
        data['created_on'] = current_time

        if POSTGRES.insert('liquid_1_activities', data, 'liquid_1_activity_id'):

            return 1

    elif partition == 'data%23da':

        data['liquid_2_activity_id'] = SHA_SECURITY.generate_token(False)
        data['establ_id'] = estab_id
        data['syst_id'] = system_id
        data['results'] = json.dumps(results)
        data['date_of_data'] = timestamp
        data['update_on'] = current_time
        data['created_on'] = current_time

        if POSTGRES.insert('liquid_2_activities', data, 'liquid_2_activity_id'):

            return 1

    return 0


def days_update(timestamp, count=0, add=False):
    """Days Update"""
    try:

        named_tuple = time.localtime(int(timestamp))

        # GET YEAR MONTH DAY
        year = int(time.strftime("%Y", named_tuple))
        month = int(time.strftime("%m", named_tuple))
        day = int(time.strftime("%d", named_tuple))

        # Date in tuple
        date_tuple = (year, month, day, 0, 0, 0, 0, 0, 0)

        local_time = time.mktime(date_tuple)
        orig = datetime.fromtimestamp(local_time)

        if add:

            new = orig + timedelta(days=count)

        else:

            new = orig - timedelta(days=count)

        return new.timestamp()

    except:

        return 0

def get_calculation(partition, value, estab_id, system_id):


    results = {}

    if partition == 'data%23wa':

        sql_str = "SELECT * FROM w_activities WHERE"
        sql_str += " establ_id='{0}' AND".format(estab_id)
        sql_str += " syst_id='{0}'".format(system_id)
        sql_str += " ORDER BY date_of_data LIMIT 1"
        w_activities = POSTGRES.query_fetch_one(sql_str)

        flow_output = 0

        if w_activities:

            flow_output = float_data(w_activities['results']['flow_output'])

        # EACH VALUES


        flow_output += float_data(value['flow_output'].split("L")[0])

        if value['reason'].upper() == 'FLUSH':

            timestamp = time.time()
            wdata = {}
            wdata['wf_activity_id'] = value['_id']
            wdata['establ_id'] = value['establishment_id']
            wdata['syst_id'] = value['system_id']
            wdata['duration'] = value['duration']
            wdata['temperature'] = value['temperature']
            wdata['type'] = value['type']
            wdata['reason'] = value['reason']
            wdata['flow_output'] = value['flow_output']
            wdata['date_of_data'] = int(value['timestamp'])
            wdata['update_on'] = timestamp
            wdata['created_on'] = timestamp

            # SAVE
            POSTGRES.insert('wf_activities', wdata, 'wf_activity_id')

        elif value['reason'].upper() == 'THERMAL DISINFECTION':

            timestamp = time.time()
            wdata = {}
            wdata['wt_activity_id'] = value['_id']
            wdata['establ_id'] = value['establishment_id']
            wdata['syst_id'] = value['system_id']
            wdata['duration'] = value['duration']
            wdata['temperature'] = value['temperature']
            wdata['type'] = value['type']
            wdata['reason'] = value['reason']
            wdata['flow_output'] = value['flow_output']
            wdata['date_of_data'] = int(value['timestamp'])
            wdata['update_on'] = timestamp
            wdata['created_on'] = timestamp

            # SAVE
            POSTGRES.insert('wt_activities', wdata, 'wt_activity_id')

        results['flow_output'] = flow_output

    elif partition == 'data%23sa':

        sql_str = "SELECT * FROM liquid_1_activities WHERE"
        sql_str += " establ_id='{0}' AND".format(estab_id)
        sql_str += " syst_id='{0}'".format(system_id)
        sql_str += " ORDER BY date_of_data LIMIT 1"
        liquid_1_activities = POSTGRES.query_fetch_one(sql_str)

        liquid1 = 0

        if liquid_1_activities:

            liquid1 = float_data(liquid_1_activities['results']['liquid1'])

        if value:

            try:

                liquid1 += float_data(value['liquid_1_dose'])

            except:

                pass

            try:

                liquid1 += float_data(value['liquid_1_dose'])

            except:

                pass

        results['liquid1'] = liquid1

    elif partition == 'data%23da':

        sql_str = "SELECT * FROM liquid_2_activities WHERE"
        sql_str += " establ_id='{0}' AND".format(estab_id)
        sql_str += " syst_id='{0}'".format(system_id)
        sql_str += " ORDER BY date_of_data LIMIT 1"
        liquid_2_activities = POSTGRES.query_fetch_one(sql_str)

        liquid2 = 0

        if liquid_2_activities:

            liquid2 = float_data(liquid_2_activities['results']['liquid2'])


        if value:

            try:

                liquid2 += float_data(value['liquid_2_dose'])

            except:

                pass

            try:

                liquid2 += float_data(value['liquid_2_dose'])

            except:

                pass

        results['liquid2'] = liquid2

    else:

        print("Invalid partition: ", partition)

    return results

def update_results(estab_id, system_id, partition, timestamp, results):
    """ SAVE RESULTS """

    data = {}
    current_time = time.time()

    if partition == 'data%23wa':

        sql_str = "SELECT * FROM w_activities WHERE"
        sql_str += " establ_id='{0}' AND".format(estab_id)
        sql_str += " syst_id='{0}'".format(system_id)
        sql_str += " ORDER BY date_of_data LIMIT 1"
        w_activities = POSTGRES.query_fetch_one(sql_str)

        data['results'] = json.dumps(results)
        data['update_on'] = current_time

        # CONDITIONS
        conditions = []

        conditions.append({
            "col": "w_activity_id",
            "con": "=",
            "val": w_activities['w_activity_id']})

        if POSTGRES.update('w_activities', data, conditions):

            return 1

    elif partition == 'data%23sa':

        sql_str = "SELECT * FROM liquid_1_activities WHERE"
        sql_str += " establ_id='{0}' AND".format(estab_id)
        sql_str += " syst_id='{0}'".format(system_id)
        sql_str += " ORDER BY date_of_data LIMIT 1"
        liquid_1_activities = POSTGRES.query_fetch_one(sql_str)

        data['results'] = json.dumps(results)
        data['update_on'] = current_time

        # CONDITIONS
        conditions = []

        conditions.append({
            "col": "liquid_1_activity_id",
            "con": "=",
            "val": liquid_1_activities['liquid_1_activity_id']})

        if POSTGRES.update('liquid_1_activities', data, conditions, log=True):

            return 1

    elif partition == 'data%23da':

        sql_str = "SELECT * FROM liquid_2_activities WHERE"
        sql_str += " establ_id='{0}' AND".format(estab_id)
        sql_str += " syst_id='{0}'".format(system_id)
        sql_str += " ORDER BY date_of_data LIMIT 1"
        liquid_2_activities = POSTGRES.query_fetch_one(sql_str)

        data['results'] = json.dumps(results)
        data['update_on'] = current_time

        # CONDITIONS
        conditions = []

        conditions.append({
            "col": "liquid_2_activity_id",
            "con": "=",
            "val": liquid_2_activities['liquid_2_activity_id']})

        if POSTGRES.update('liquid_2_activities', data, conditions, log=True):

            return 1

    return 0

def get_default_network():
    """ RETURN DEFAULT NETWORK """

    # GET DEFAULT NETWORK ID
    sql_str = "SELECT network_id FROM network WHERE"
    sql_str += " network_name='DEFAULT' AND default_value=True"
    network = POSTGRES.query_fetch_one(sql_str)

    return network['network_id']


def format_units(value, unit):
    """ Return value with unit """

    data = "{0} {1}".format(value, unit)
    if float(value) > 1:
        data = "{0} {1}s".format(value, unit)

    return data

def validate_data(data):
    """ Validate Data"""

    tmp = {}
    if "soap_dose" in data:

        tmp['soap_dose'] = data['soap_dose']
        if "milliliter" not in data['soap_dose']:
            tmp['soap_dose'] = format_units(data['soap_dose'], "milliliter")

    if "disinfect_dose" in data:
        tmp['disinfect_dose'] = data['disinfect_dose']
        if "milliliter" not in data['disinfect_dose']:
            tmp['disinfect_dose'] = format_units(data['disinfect_dose'], "milliliter")

    if "init_wtr_temp" in data:

        tmp['init_wtr_temp'] = data['init_wtr_temp']
        if type(data['init_wtr_temp']) == int:
            if data['init_wtr_temp'] <= 2:
                tmp['init_wtr_temp'] = "{0} (cold)".format(data['init_wtr_temp'])

            if data['init_wtr_temp'] >=3 and data['init_wtr_temp'] <=7:
                tmp['init_wtr_temp'] = "{0} (lukewarm)".format(data['init_wtr_temp'])

            if data['init_wtr_temp'] >=8:
                tmp['init_wtr_temp'] = "{0} (hot)".format(data['init_wtr_temp'])

    if "wtr_shut_off_dly" in data:

        tmp['wtr_shut_off_dly'] = data['wtr_shut_off_dly']
        if type(data['wtr_shut_off_dly']) == int:
            tmp['wtr_shut_off_dly'] = format_units(data['wtr_shut_off_dly'], "second")

    if "wtr_temp_mem_tm" in data:

        tmp['wtr_temp_mem_tm'] = data['wtr_temp_mem_tm']
        if type(data['wtr_temp_mem_tm']) == int:
            tmp['wtr_temp_mem_tm'] = format_units(data['wtr_temp_mem_tm'], "second")

    if "bucket_mode_d" in data:

        tmp['bucket_mode_d'] = data['bucket_mode_d']
        if type(data['bucket_mode_d']) == int:
            tmp['bucket_mode_d'] = format_units(data['bucket_mode_d'], "minutes")

    if "tm_b4_stagn_flsh" in data:

        tmp['tm_b4_stagn_flsh'] = data['tm_b4_stagn_flsh']
        if type(data['tm_b4_stagn_flsh']) == int:
            tmp['tm_b4_stagn_flsh'] =  format_units(data['tm_b4_stagn_flsh'], "hour")

    if "stagn_flsh_d" in data:

        tmp['stagn_flsh_d'] = data['stagn_flsh_d']

        if "minute"  not in data['stagn_flsh_d']:
            tmp['stagn_flsh_d'] =  format_units(data['stagn_flsh_d'], "minute")

    if "stagn_flsh_u_dep" in data:

        tmp['stagn_flsh_u_dep'] = data['stagn_flsh_u_dep']
        if data['stagn_flsh_u_dep'] == 0:
            tmp['stagn_flsh_u_dep'] = "No"

        if data['stagn_flsh_u_dep'] == 1:
            tmp['stagn_flsh_u_dep'] = "Yes"

    if "thrm_flshng_tm" in data:

        tmp['thrm_flshng_tm'] = data['thrm_flshng_tm']
        if "At" not in data['thrm_flshng_tm']:
            tmp['thrm_flshng_tm'] = "At {0}".format(data['thrm_flshng_tm'])

    if "thrm_flshng_day" in data:

        tmp['thrm_flshng_day'] = data

        if data['thrm_flshng_day'] == 0:
            tmp['thrm_flshng_day'] = "Off"

        if data['thrm_flshng_day'] == 1:
            tmp['thrm_flshng_day'] = "Every Monday"

        if data['thrm_flshng_day'] == 2:
            tmp['thrm_flshng_day'] = "Every Tuesday"

        if data['thrm_flshng_day'] == 3:
            tmp['thrm_flshng_day'] = "Every Wednesday"

        if data['thrm_flshng_day'] == 4:
            tmp['thrm_flshng_day'] = "Every Thursday"

        if data['thrm_flshng_day'] == 5:
            tmp['thrm_flshng_day'] = "Every Friday"

        if data['thrm_flshng_day'] == 6:
            tmp['thrm_flshng_day'] = "Every Saturday"

        if data['thrm_flshng_day'] == 7:
            tmp['thrm_flshng_day'] = "Every Sunday"

        if data['thrm_flshng_day'] == 8:
            tmp['thrm_flshng_day'] = "Every second Monday"

        if data['thrm_flshng_day'] == 9:
            tmp['thrm_flshng_day'] = "Every second Tuesday"

        if data['thrm_flshng_day'] == 10:
            tmp['thrm_flshng_day'] = "Every second Wednesday"

        if data['thrm_flshng_day'] == 11:
            tmp['thrm_flshng_day'] = "Every second Thursday"

        if data['thrm_flshng_day'] == 12:
            tmp['thrm_flshng_day'] = "Every second Friday"

        if data['thrm_flshng_day'] == 13:
            tmp['thrm_flshng_day'] = "Every second Saturday"

        if data['thrm_flshng_day'] == 14:
            tmp['thrm_flshng_day'] = "Every second Sunday"

        if data['thrm_flshng_day'] == 15:
            tmp['thrm_flshng_day'] = "Every third Monday"

        if data['thrm_flshng_day'] == 16:
            tmp['thrm_flshng_day'] = "Every third Tuesday"

        if data['thrm_flshng_day'] == 17:
            tmp['thrm_flshng_day'] = "Every third Wednesday"

        if data['thrm_flshng_day'] == 18:
            tmp['thrm_flshng_day'] = "Every third Thursday"

        if data['thrm_flshng_day'] == 19:
            tmp['thrm_flshng_day'] = "Every third Friday"

        if data['thrm_flshng_day'] == 20:
            tmp['thrm_flshng_day'] = "Every third Saturday"

        if data['thrm_flshng_day'] == 21:
            tmp['thrm_flshng_day'] = "Every third Sunday"

        if data['thrm_flshng_day'] == 22:
            tmp['thrm_flshng_day'] = "Coming Monday (single flush)"

        if data['thrm_flshng_day'] == 23:
            tmp['thrm_flshng_day'] = "Coming Tuesday (single flush)"

        if data['thrm_flshng_day'] == 24:
            tmp['thrm_flshng_day'] = "Coming Wednesday (single flush)"

        if data['thrm_flshng_day'] == 25:
            tmp['thrm_flshng_day'] = "Coming Thursday (single flush)"

        if data['thrm_flshng_day'] == 26:
            tmp['thrm_flshng_day'] = "Coming Friday (single flush)"

        if data['thrm_flshng_day'] == 27:
            tmp['thrm_flshng_day'] = "Coming Saturday (single flush)"

        if data['thrm_flshng_day'] == 28:
            tmp['thrm_flshng_day'] = "Coming Sunday (single flush)"

        if data['thrm_flshng_day'] == 29:
            tmp['thrm_flshng_day'] = "Monthly every Monday"

        if data['thrm_flshng_day'] == 30:
            tmp['thrm_flshng_day'] = "Monthly every Tuesday"

        if data['thrm_flshng_day'] == 31:
            tmp['thrm_flshng_day'] = "Monthly every Wednesday"

        if data['thrm_flshng_day'] == 32:
            tmp['thrm_flshng_day'] = "Monthly every Thursday"

        if data['thrm_flshng_day'] == 33:
            tmp['thrm_flshng_day'] = "Monthly every Friday"

        if data['thrm_flshng_day'] == 34:
            tmp['thrm_flshng_day'] = "Monthly every Saturday"

        if data['thrm_flshng_day'] == 35:
            tmp['thrm_flshng_day'] = "Monthly every Sunday"

        if data['thrm_flshng_day'] == 36:
            tmp['thrm_flshng_day'] = "Monday every 6 weeks"

        if data['thrm_flshng_day'] == 37:
            tmp['thrm_flshng_day'] = "Tuesday every 6 weeks"

        if data['thrm_flshng_day'] == 38:
            tmp['thrm_flshng_day'] = "Wednesday every 6 weeks"

        if data['thrm_flshng_day'] == 39:
            tmp['thrm_flshng_day'] = "Thursday every 6 weeks"

        if data['thrm_flshng_day'] == 40:
            tmp['thrm_flshng_day'] = "Friday every 6 weeks"

        if data['thrm_flshng_day'] == 41:
            tmp['thrm_flshng_day'] = "Saturday every 6 weeks"

        if data['thrm_flshng_day'] == 42:
            tmp['thrm_flshng_day'] = "Sunday every 6 weeks"

        if data['thrm_flshng_day'] == 43:
            tmp['thrm_flshng_day'] = "Monday every 2 months"

        if data['thrm_flshng_day'] == 44:
            tmp['thrm_flshng_day'] = "Tuesday every 2 months"

        if data['thrm_flshng_day'] == 45:
            tmp['thrm_flshng_day'] = "Wednesday every 2 monthss"

        if data['thrm_flshng_day'] == 46:
            tmp['thrm_flshng_day'] = "Thursday every 2 months"

        if data['thrm_flshng_day'] == 47:
            tmp['thrm_flshng_day'] = "Friday every 2 months"

        if data['thrm_flshng_day'] == 48:
            tmp['thrm_flshng_day'] = "Saturday every 2 months"

        if data['thrm_flshng_day'] == 49:
            tmp['thrm_flshng_day'] = "Sunday every 2 months"

    if "thrm_flsh_temp" in data:

        tmp['thrm_flsh_temp'] =  data['thrm_flsh_temp']
        if "Degrees Celsius" not in data['thrm_flsh_temp']:
            tmp['thrm_flsh_temp'] = "{0} thrm_flsh_temp".format(data['thrm_flsh_temp'])

    if "thrm_flsh_d" in data:

        tmp['thrm_flsh_d'] = data['thrm_flsh_d']
        if type(data['thrm_flsh_d']) == int:

            temp = round(float(data['thrm_flsh_d'] / 60), 2)
            tmp['thrm_flsh_d'] = "{0} minutes".format(temp)

            if float(temp) <= 1:
                tmp['thrm_flsh_d'] = "{0} minute".format(temp)

    if "light_effect" in data:

        tmp['light_effect'] = data['light_effect']
        if data['light_effect'] == 0:
            tmp['light_effect'] = "Off"

        if data['light_effect'] == 1:
            tmp['light_effect'] = "On"

        if data['light_effect'] == 2:
            tmp['light_effect'] = "Pulse"

    if "beep_tone" in data:

        tmp['beep_tone'] = data['beep_tone']
        if data['beep_tone'] == 0:
            tmp['beep_tone'] = "Off"

        if type(data['beep_tone']) == int:
            tmp['beep_tone'] = "Level {0}".format(data['beep_tone'])


    if "clean_mode" in data:

        tmp['clean_mode'] = data['clean_mode']
        if data['clean_mode'] == 0:
            tmp['clean_mode'] = "Off"

        if data['clean_mode'] == 1:
            tmp['clean_mode'] = "ON"


    if "flow_heater_mode" in data:

        tmp['flow_heater_mode'] = data['flow_heater_mode']
        if data['flow_heater_mode'] == 0:
            tmp['flow_heater_mode'] = "Off"

        if data['flow_heater_mode'] == 1:
            tmp['flow_heater_mode'] = "ON"

    if "ir_range" in data:

        tmp['ir_range'] = data['ir_range']
        if type(data['ir_range']) == int:
            tmp['ir_range'] = format_units(data['ir_range'], "centimeter")

    return tmp
