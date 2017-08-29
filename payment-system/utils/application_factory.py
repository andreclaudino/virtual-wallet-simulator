from controller.user_controller import user_blueprint
from flask_api import FlaskAPI

from controller.root_controller import root_blueprint


def create_app():
    app = FlaskAPI(__name__)

    # Default route (principal api)
    app.register_blueprint(user_blueprint, url_prefix='/user')
    app.register_blueprint(root_blueprint, url_prefix='')

    # V1 Api
    app.register_blueprint(user_blueprint, url_prefix='/v1/user')
    app.register_blueprint(root_blueprint, url_prefix='/v1')


    return app
