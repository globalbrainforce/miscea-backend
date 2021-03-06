# pylint: disable=no-self-use, too-many-arguments, too-many-branches, too-many-public-methods, bare-except, unidiomatic-typecheck, no-member, anomalous-backslash-in-string
"""Common"""
import time
import pytz

from datetime import datetime, timedelta
import re
import simplejson
import dateutil.relativedelta

from flask import jsonify
from library.log import Log
from library.postgresql_queries import PostgreSQL

class Common():
    """Class for Common"""

    # INITIALIZE
    def __init__(self):
        """The Constructor for Common class"""
        self.log = Log()
        self.epoch_default = 26763
        self.postgres = PostgreSQL()

    # RETURN DATA
    def return_data(self, data):
        """Return Data"""
        # RETURN
        return jsonify(
            data
        )

    # REMOVE KEY
    def remove_key(self, data, item):
        """Remove Key"""

        # CHECK DATA
        if item in data:

            # REMOVE DATA
            del data[item]

        # RETURN
        return data


    def isfloat(self, data):
        """Check if float"""
        try:
            if data == "infinity":
                return False

            float(data)
        except ValueError:
            return False
        else:
            return True

    def isint(self, data):
        """Check if Integer"""
        try:
            if data == "infinity":
                return False

            tmp_data1 = float(data)
            tmp_data2 = int(tmp_data1)
        except ValueError:
            return False
        else:
            return tmp_data1 == tmp_data2

    def limits(self, rows, limit, page):
        """Limits"""
        skip = int((page - 1) * limit)

        limit = skip + limit

        return rows[skip:limit]

    def validate_default_token(self, token):
        """ VALIDATE DEFAULT TOKEN """

        sql_str = "SELECT token_id FROM default_tokens WHERE"
        sql_str += " token='{0}'".format(token)

        if self.postgres.query_fetch_one(sql_str):

            return 1

        return 0

    def validate_tap_token(self, token, system_id):
        """ VALIDATE DEFAULT TOKEN """

        sql_str = "SELECT tap_account_id FROM tap_accounts WHERE"
        sql_str += " token='{0}'".format(token)

        if self.postgres.query_fetch_one(sql_str):

            tap_account = {}
            tap_account['system_id'] = system_id
            tap_account['token'] = token
            tap_account['last_login'] = time.time()

            sql_str = "SELECT tap_account_id FROM tap_accounts WHERE"
            sql_str += " system_id='{0}'".format(system_id)
            response = self.postgres.query_fetch_one(sql_str)

            if response:

                # INIT CONDITION
                conditions = []

                # CONDITION FOR QUERY
                conditions.append({
                    "col": "tap_account_id",
                    "con": "=",
                    "val": response['tap_account_id']
                    })

                # UPDATE TAP ACCOUNT TOKEN
                tap_account['token'] = token
                tap_account['update_on'] = time.time()

                self.postgres.update('tap_accounts', tap_account, conditions)

            else:

                # INSERT TAP ACCOUNT TOKEN
                tap_account['tap_account_id'] = SHASECURITY.generate_token(False)
                tap_account['created_on'] = time.time()

                self.postgres.insert('tap_accounts', tap_account)

            return 1

        return 0

    def get_epoch_date_hour(self, epoch_date, tz='Europe/Amsterdam'):
        """ Return Formatted Date and Hours"""

        tztimestamp = pytz.timezone(tz)

        formatted = {}

        formatted['date'] = datetime.fromtimestamp(int(epoch_date), tztimestamp).strftime('%d.%m.%Y')
        formatted['time'] = datetime.fromtimestamp(int(epoch_date), tztimestamp).strftime('%I:%M')
        formatted['meridian'] = datetime.fromtimestamp(int(epoch_date), tztimestamp).strftime('%p')

        return formatted
