from base.connect_db import ConnectDB
from utils.application_factory import create_app

# === Script to launch server ===

"""
This script launches payment-system server from configurations
using configurations returned by server_config().
"""

def runner(env=None, response=None):
    ConnectDB.connect_database()

    app = create_app()
    app.run()

if __name__ == '__main__':
    runner()
