from base.connect_db import ConnectDB
from utils.application_factory import create_app

# === Script to launch server ===

"""
This script launches payment-system server from configurations
using configurations returned by server_config().
"""


ConnectDB.connect_database()

app = create_app()

