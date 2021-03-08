#====================================#
# AUTHOR:      KRISFEN DUCAO         #
#====================================#
# pylint: disable=too-many-arguments, too-many-branches, invalid-name
"""Couch Queries"""
import json
import syslog
import requests
from library.couch_database import CouchDatabase
from library.common import Common

class Queries(Common):
    """Class for Queries"""

    # INITIALIZE
    def __init__(self):
        """The Constructor for Vessels class"""
        self._couch_db = CouchDatabase()
        super(Queries, self).__init__()

    def get_by_id(self, couch_id, db=None):
        """Get By ID"""
        couch_query = self._couch_db.couch_db_link()

        if db:

            couch_query = self._couch_db.couch_db_link(db)

        couch_query += '/' + str(couch_id)

        # EXECUTE COUCH QUERY
        res = requests.get(couch_query)
        json_data = res.json()

        if json_data:

            return json_data

        return {}

    def get_establishments(self, estab_id=None, limit=None, page=None, db=None):
        """Return Establishment"""
        # COUCH QUERY - GET ESTABLISHMENT
        couch_query = self._couch_db.couch_db_link()

        if db:

            couch_query = self._couch_db.couch_db_link(db)

        couch_query += '/_partition/establishment/_design/establishments/'
        couch_query += '_view/get_establishments?'
        if estab_id:
            couch_query += 'startkey="' + estab_id + '"'
            couch_query += '&endkey="' + estab_id + '"&'

        couch_query += 'include_docs=true'

        # EXECUTE COUCH QUERY
        res = requests.get(couch_query)
        json_data = res.json()

        if limit and page:

            rows = json_data['rows']
            establishments = self.limits(rows, limit, page)

        else:

            establishments = json_data['rows']

        return establishments

    def get_system_installed(self, sys_id=None, limit=None, page=None, db=None):
        """Return System Installed"""

        couch_query = self._couch_db.couch_db_link()

        if db:

            couch_query = self._couch_db.couch_db_link(db)

        couch_query += '/_partition/system/_design/systems/'
        couch_query += '_view/get_systems?'
        if sys_id:
            couch_query += 'startkey="' + sys_id + '"'
            couch_query += '&endkey="' + sys_id + '"&'

        couch_query += 'include_docs=true'

        # EXECUTE COUCH QUERY
        res = requests.get(couch_query)
        json_data = res.json()

        if limit and page:

            rows = json_data['rows']
            systems = self.limits(rows, limit, page)

        else:

            systems = json_data['rows']

        return systems

    def get_systems(self, estab_id, db=None):
        """Return All Systems"""
        # COUCH QUERY - GET ESTABLISHMENT
        couch_query = self._couch_db.couch_db_link()

        if db:

            couch_query = self._couch_db.couch_db_link(db)

        couch_query += '/_partition/system/_design/systems/'
        couch_query += '_view/get_systems?'
        couch_query += 'startkey=["' + estab_id + '"]&'
        couch_query += 'endkey=["' + estab_id + '",{}]&'
        couch_query += 'include_docs=true'

        # EXECUTE COUCH QUERY
        res = requests.get(couch_query)
        json_data = res.json()
        systems = json_data['rows']

        return systems


    def get_complete_values(self, estab_id, system_id, partition, start=None,
                            end=None, flag='one', descending=True, db=None):
        """Return Complete Values"""
        couch_query = self._couch_db.couch_db_link()

        if db:

            couch_query = self._couch_db.couch_db_link(db)

        couch_query += '/_partition/{0}/_design/data/'.format(partition)
        couch_query += '_view/get_datas?'

        if start and end:
            couch_query += 'startkey=["{0}","{1}",{2}]&'.format(estab_id, system_id, end)
            couch_query += 'endkey=["{0}","{1}",{2}]'.format(estab_id, system_id, start)

            if flag == 'all':

                couch_query += '&include_docs=true&descending=true'

            else:
                if descending:

                    couch_query += '&include_docs=true&limit=1&descending=true'

                else:

                    couch_query += '&include_docs=true&limit=1'

        else:
            couch_query += 'startkey=["' + estab_id + '", "' + system_id + '",9999999999]&'
            couch_query += 'endkey=["' + estab_id + '", "' + system_id + '",0]'

            if flag == 'all':
                couch_query += '&include_docs=true&descending=true'
            else:
                couch_query += '&include_docs=true&limit=1&descending=true'

        res = requests.get(couch_query)
        json_data = res.json()
        data = []

        if 'rows' not in json_data.keys():

            print("Error: {0}".format(json_data))

        else:
            rows = json_data['rows']

            if rows:

                if flag == 'one':

                    if rows:
                        data = rows[0]['doc']

                if flag == 'one_doc':

                    if rows:
                        data = rows[0]['doc']

                elif flag == 'all':

                    data = []
                    for row in rows:

                        data.append(row['doc'])

        return data

    def latest_datas(self, estab_id, system_id, partition, start=None,
                     end=None, limit=None, descending=True, db=None):
        """Return Complete Values"""
        couch_query = self._couch_db.couch_db_link()

        if not limit:
            limit = 1

        if db:

            couch_query = self._couch_db.couch_db_link(db)

        couch_query += '/_partition/{0}/_design/data/'.format(partition)
        couch_query += '_view/get_datas?'

        if start and end:
            couch_query += 'startkey=["{0}","{1}",{2}]&'.format(estab_id, system_id, end)
            couch_query += 'endkey=["{0}","{1}",{2}]'.format(estab_id, system_id, start)

            if descending:

                couch_query += '&include_docs=true&limit={0}&descending=true'.format(limit)

            else:

                couch_query += '&include_docs=true&limit={0}'.format(limit)

        else:
            couch_query += 'startkey=["' + estab_id + '", "' + system_id + '",{}]&'
            couch_query += 'endkey=["' + estab_id + '", "' + system_id + '"]'

            couch_query += '&include_docs=true&limit={0}&descending=true'.format(limit)

        res = requests.get(couch_query)
        json_data = res.json()
        data = []

        if 'rows' not in json_data.keys():

            print("Error: {0}".format(json_data))

        else:
            rows = json_data['rows']

            if rows:

                data = []
                for row in rows:

                    data.append(row['doc'])

        return data

    def all_docs(self, ids):

        couch_query = self._couch_db.couch_db_link()
        couch_query += "/_all_docs?include_docs=true"
        data = {'keys': ids}
        headers = {"Content-Type" : "application/json"}
        x = requests.post(couch_query, data = json.dumps(data), headers=headers)

        return x.json()

    def update(self, data, doc_id):

        # data = {}
        # data['firstname'] = 'Roel'
        # data['lastname'] = 'San Jose'
        # data['address'] = 'Palawan'
        # data['type'] = 'admin'
        # data['_rev'] = '1-175ad67e5ec8560211bbe7bc16ceebb0'

        # url = 'http://admin:admin@' + ip + ':5984/' + database_name
        couch_query = self._couch_db.couch_db_link()
        couch_query += '/'+ str(doc_id)

        headers = {"Content-Type" : "application/json"}
        r = requests.put(couch_query, data=json.dumps(data),headers=headers)
        json_data =   r.json()

        return json_data
