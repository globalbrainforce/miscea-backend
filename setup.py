# pylint: disable=too-many-locals, line-too-long, too-many-statements, too-many-branches, too-many-instance-attributes, attribute-defined-outside-init, no-self-use
"""Set Up"""
import time
from configparser import ConfigParser

from library.config_parser import config_section_parser
from library.postgresql_queries import PostgreSQL
from library.sha_security import ShaSecurity
from library.log import Log

class Setup():
    """Class for Setup"""

    def __init__(self):
        """The constructor for Setup class"""
        self.sha_security = ShaSecurity()
        self.postgres = PostgreSQL()

        # INIT CONFIG
        self.config = ConfigParser()
        # CONFIG FILE
        self.config.read("config/config.cfg")
        self.log = Log()

    def main(self):
        """Main"""
        self.create_database()
        self.create_tables()
        self.create_default_entries()

    def create_database(self):
        """Create Database"""
        self.dbname = config_section_parser(self.config, "POSTGRES")['db_name']
        self.postgres.connection(True)
        self.postgres.create_database(self.dbname)
        self.postgres.close_connection()

    def create_tables(self):
        """Create Tables"""

        # OPEN CONNECTION
        self.postgres.connection()

        # DEFAULT TOKENS TABLE
        query_str = "CREATE TABLE default_tokens (token_id VARCHAR (1000) PRIMARY KEY,"
        query_str += " token VARCHAR (1000) UNIQUE NOT NULL,"
        query_str += " default_value BOOLEAN,"
        query_str += " created_on BIGINT NOT NULL,"
        query_str += " update_on BIGINT)"

        # TAP ACCOUNTS TABLE
        query_str = "CREATE TABLE tap_accounts (tap_account_id VARCHAR (1000) PRIMARY KEY,"
        query_str += " token VARCHAR (1000),"
        query_str += " created_on BIGINT NOT NULL,"
        query_str += " update_on BIGINT, last_login BIGINT)"

        print("Create table: tap_accounts")
        if self.postgres.exec_query(query_str):
            self.log.info("Tap Accounts table successfully created!")

    def create_default_entries(self):
        """ CREATE DEFAULT ENTRIES """

        for dta in range(1, 16):

            data1 = {}
            data1['token_id'] = self.sha_security.generate_token(False)
            data1['token'] = config_section_parser(self.config, "TOKENS")['token' + str(dta)]
            data1['default_value'] = True
            data1['created_on'] = time.time()

            print("Create default token {0}".format(dta))
            self.postgres.insert('default_tokens', data1)
