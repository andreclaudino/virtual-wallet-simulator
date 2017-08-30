import os
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
        return dict(url=os.environ.get("GRAPHENEDB_BOLT_URL"),
                    user=os.environ.get("GRAPHENEDB_BOLT_USER"),
                    password=os.environ.get("GRAPHENEDB_BOLT_PASSWORD"))

    # === database connector ===
    @staticmethod
    def connect_database():
        """
        Estabilish connection to Neo4J database based on configuration file
        """
        file_config = ConnectDB.load_default_config()
        neomodel.config.DATABASE_URL =\
            'bolt://{user}:{password}@{url}'.format(**file_config)
