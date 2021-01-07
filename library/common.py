# pylint: disable=no-self-use, too-many-arguments, too-many-branches, too-many-public-methods, bare-except, unidiomatic-typecheck, no-member, anomalous-backslash-in-string
"""Common"""
import time
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
        sql_str += " system_id='{0}'".format(system_id)
        sql_str += " AND token='{0}'".format(token)

        if self.postgres.query_fetch_one(sql_str):

            return 1

        return 0
