import json
import neomodel.config

"""
ConnectDB:
created by André Claudino <claudino@d2x.com.br>
"""

class ConnectDB:
    """
    ConnectDB:
    this class is used to read configuration file and set connection
    to Neo4j database.
    """

    @staticmethod
    def load_default_config():
        """
        Load configuration from *db_credentials.json* file in working directory
        :return: dictionary of database connection configuration
        """
        with open('db_credentials.json') as f:
            return json.load(f)

    @staticmethod
    def connect_database():
        """
        Estabilish connection to Neo4J database based on configuration file
        :return: None
        """
        file_config = ConnectDB.load_default_config()
        neomodel.config.DATABASE_URL =\
            '{protocol}://{user}:{password}@{url}'.format(**file_config)
