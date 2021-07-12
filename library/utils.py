class Utils():
    """Class for Utils"""

    # INITIALIZE
    def __init__(self):
        """The Constructor for Utils class"""
        super(Utils, self).__init__()

    def data_log(self, data='', divider=False):
        """ DATA LOG """

        with open('/home/admin/miscea-backend/logs.txt',"a+") as output_file:

            div = "*"*100

            if divider:

                output_file.write('{0}\n'.format(div))

            else:

                output_file.write('{0}\n'.format(data))

        return 1

    def revalidate_data(self, data):
        """ Validate Data"""

        tmp = {}
        if "soap_dose" in data:
            tmp['soap_dose'] = data['soap_dose']
            if not type(data['soap_dose']) in [int, float]:
                tmp['soap_dose'] = reformat_units(data['soap_dose'])

        if "disinfect_dose" in data:
            tmp['disinfect_dose'] = data['disinfect_dose']
            if not type(data['disinfect_dose']) in [int, float]:
                if data['disinfect_dose'] != "":

                    tmp['disinfect_dose'] = reformat_units(data['disinfect_dose'])

                else:

                    tmp['disinfect_dose'] = data['disinfect_dose']

        if "init_wtr_temp" in data:

            tmp['init_wtr_temp'] = data['init_wtr_temp']
            if not type(data['init_wtr_temp']) == int:

                if data['init_wtr_temp'] != "":

                    tmp['init_wtr_temp'] = reformat_units(data['init_wtr_temp'])

                else:

                    tmp['init_wtr_temp'] = data['init_wtr_temp']

        if "wtr_shut_off_dly" in data:

            tmp['wtr_shut_off_dly'] = data['wtr_shut_off_dly']
            if not type(data['wtr_shut_off_dly']) == int:

                if data['wtr_shut_off_dly'] != "":

                    tmp['wtr_shut_off_dly'] = reformat_units(data['wtr_shut_off_dly'])

                else:

                    tmp['wtr_shut_off_dly'] = data['wtr_shut_off_dly']

        if "wtr_temp_mem_tm" in data:

            tmp['wtr_temp_mem_tm'] = data['wtr_temp_mem_tm']
            if not type(data['wtr_temp_mem_tm']) == int:

                if data['wtr_temp_mem_tm'] != "":

                    tmp['wtr_temp_mem_tm'] = reformat_units(data['wtr_temp_mem_tm'])

                else:

                    tmp['wtr_temp_mem_tm'] = data['wtr_temp_mem_tm']

        if "bucket_mode_d" in data:

            tmp['bucket_mode_d'] = data['bucket_mode_d']
            if not type(data['bucket_mode_d']) in [int, float]:

                if data['bucket_mode_d'] != "":

                    tmp['bucket_mode_d'] = reformat_units(data['bucket_mode_d'])

                else:

                    tmp['bucket_mode_d'] = data['bucket_mode_d']

        if "tm_b4_stagn_flsh" in data:

            tmp['tm_b4_stagn_flsh'] = data['tm_b4_stagn_flsh']
            if not type(data['tm_b4_stagn_flsh']) == int:
                tmp['tm_b4_stagn_flsh'] =  reformat_units(data['tm_b4_stagn_flsh'])

        if "stagn_flsh_d" in data:

            tmp['stagn_flsh_d'] = data['stagn_flsh_d']
            if not type(data['stagn_flsh_d']) == int:
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

                duration = data['thrm_flsh_d'].split(" ")[0]
                mduration = duration.split(":")[0]
                sduration = duration.split(":")[1]
                total_duration = int(mduration) * 60
                if int(sduration) > 0:
                    total_duration += 30

                tmp['thrm_flsh_d'] = total_duration

        if "light_effect" in data:

            tmp['light_effect'] = data['light_effect']
            if data['light_effect'] == "Off":
                tmp['light_effect'] = 0

            if data['light_effect'] == "Pulse":
                tmp['light_effect'] = 1

            if data['light_effect'] == "On":
                tmp['light_effect'] = 2

        if "beep_tone" in data:

            tmp['beep_tone'] = data['beep_tone']
            if data['beep_tone'] == "Off":
                tmp['beep_tone'] = 0

            if not type(tmp['beep_tone']) == int:
                tmp['beep_tone'] = int(data['beep_tone'].split(" ")[1])

        if "clean_mode" in data:

            if data['clean_mode'] != "":

                tmp['clean_mode'] = data['clean_mode']
                if data['clean_mode'] == "Off":
                    tmp['clean_mode'] = 0

                if data['clean_mode'] == "On":
                    tmp['clean_mode'] = 1

            else:

                tmp['clean_mode'] = data['clean_mode']

        if "flow_heater_mode" in data:

            if data['flow_heater_mode'] != "":

                tmp['flow_heater_mode'] = data['flow_heater_mode']
                if data['flow_heater_mode'] == "Off":
                    tmp['flow_heater_mode'] = 0

                if data['flow_heater_mode'] == "On":
                    tmp['flow_heater_mode'] = 1

            else:

                tmp['flow_heater_mode'] = data['flow_heater_mode']

        if "ir_range" in data:

            if data['ir_range'] != "":

                tmp['ir_range'] = data['ir_range']
                if not type(data['ir_range']) in [int, float]:
                    tmp['ir_range'] = reformat_units(data['ir_range'])

            else:

                tmp['ir_range'] = data['ir_range']

        if "stagn_flsh_up_power" in data:

            if data['stagn_flsh_up_power'] != "":

                tmp['stagn_flsh_up_power'] = data['stagn_flsh_up_power']
                if data['stagn_flsh_up_power'] == "Off":
                    tmp['stagn_flsh_up_power'] = 0

                if data['stagn_flsh_up_power'] == "On":
                    tmp['stagn_flsh_up_power'] = 1

            else:

                tmp['stagn_flsh_up_power'] = data['stagn_flsh_up_power']

        if "end_point_filter_mode" in data:

            if data['end_point_filter_mode'] != "":

                tmp['end_point_filter_mode'] = data['end_point_filter_mode']
                if data['end_point_filter_mode'] == "Off":
                    tmp['end_point_filter_mode'] = 0

                if data['end_point_filter_mode'] == "On":
                    tmp['end_point_filter_mode'] = 1

            else:

                tmp['end_point_filter_mode'] = data['end_point_filter_mode']

        if "hand_disinfection_tmr" in data:

            tmp['hand_disinfection_tmr'] = data['hand_disinfection_tmr']
            if not type(data['hand_disinfection_tmr']) == int:

                if data['hand_disinfection_tmr'] != "":

                    tmp['hand_disinfection_tmr'] = reformat_units(data['hand_disinfection_tmr'])

                else:

                    tmp['hand_disinfection_tmr'] = data['hand_disinfection_tmr']

        if "hand_washing_tmr" in data:

            tmp['hand_washing_tmr'] = data['hand_washing_tmr']
            if not type(data['hand_washing_tmr']) == int:

                if data['hand_washing_tmr'] != "":

                    tmp['hand_washing_tmr'] = reformat_units(data['hand_washing_tmr'])

                else:

                    tmp['hand_washing_tmr'] = data['hand_washing_tmr']

        if "public_mode" in data:

            if data['public_mode'] != "":

                tmp['public_mode'] = data['public_mode']
                if data['public_mode'] == "Off":
                    tmp['public_mode'] = 0

                if data['public_mode'] == "On":
                    tmp['public_mode'] = 1

            else:

                tmp['public_mode'] = data['public_mode']

        if "first_wtr_cycle_delay" in data:

            tmp['first_wtr_cycle_delay'] = data['first_wtr_cycle_delay']
            if not type(data['first_wtr_cycle_delay']) == int:

                if data['first_wtr_cycle_delay'] != "":

                    tmp['first_wtr_cycle_delay'] = reformat_units(data['first_wtr_cycle_delay'])

                else:

                    tmp['first_wtr_cycle_delay'] = data['first_wtr_cycle_delay']

        if "first_wtr_cycle_d" in data:

            tmp['first_wtr_cycle_d'] = data['first_wtr_cycle_d']
            if not type(data['first_wtr_cycle_d']) == int:

                if data['first_wtr_cycle_d'] != "":

                    tmp['first_wtr_cycle_d'] = reformat_units(data['first_wtr_cycle_d'])

                else:

                    tmp['first_wtr_cycle_d'] = data['first_wtr_cycle_d']

        if "second_wtr_cycle_d" in data:

            tmp['second_wtr_cycle_d'] = data['second_wtr_cycle_d']
            if not type(data['second_wtr_cycle_d']) == int:

                if data['second_wtr_cycle_d'] != "":

                    tmp['second_wtr_cycle_d'] = reformat_units(data['second_wtr_cycle_d'])

                else:

                    tmp['second_wtr_cycle_d'] = data['second_wtr_cycle_d']

        for key in tmp.keys():

            data[key] = tmp[key]

        return data

def reformat_units(value):
    """ REFORMAT """

    return float(value.split(" ")[0])
