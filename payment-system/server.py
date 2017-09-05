from base.connect_db import ConnectDB
from utils.application_factory import create_app

# === Script to launch server ===

"""
This script launches payment-system server
"""


ConnectDB.connect_database()

app = create_app()

if __name__=='__main__':
    app.run()