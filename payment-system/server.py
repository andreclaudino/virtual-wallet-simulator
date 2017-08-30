from base.connect_db import ConnectDB
from utils.application_factory import create_app
from utils.authorize import server_config



if __name__ == "__main__":

    run_config = server_config()['run_config']

    app = create_app()

    ConnectDB.connect_database()
    app.run(ssl_context=('cert.pem', 'key.pem'), **run_config)
