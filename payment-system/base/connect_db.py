import json
import neomodel.config

# === Database Connection Class ===
class ConnectDB:
    """
    ConnectDB:
    Reads db_credentials.json and connect neo4j database
    """

    # === Configuration Loader ===
    @staticmethod
    def load_default_config():
        """
        Load configuration from *db_credentials.json* file in working directory
        :return: dictionary of database connection configuration
        """
        with open('db_credentials.json') as f:
            return json.load(f)

    # === database connector ===
    @staticmethod
    def connect_database():
        """
        Estabilish connection to Neo4J database based on configuration file
        """
        file_config = ConnectDB.load_default_config()
        neomodel.config.DATABASE_URL =\
            '{protocol}://{user}:{password}@{url}'.format(**file_config)
