from flask import request

from base.base_controller import BaseController
from exceptions.user_exceptions import UsernameNotFound, UserPasswordIncorrect, UserInactive
from model.user import User
from utils.authorize import generate_auth_token

root_blueprint = BaseController('root')

@root_blueprint.route('/')
def health_check():
    return dict(api_status='OK')


@root_blueprint.route('/login', methods=['POST'])
def login():
    """
    Perform login, return Auth token + User object
    :param username: username to login
    :param password: password to login
    :return: User and object and auth_token
    """
    try:
        form = request.values

        username = form['username']
        password = form['password']

        user = User.login(username, password)
        token = generate_auth_token(user.username, user.uid)

        return dict(user=user.to_dict(), token=token.decode('ascii'))

    except UsernameNotFound as e:
        return dict(error=str(e)), 401
    except UserPasswordIncorrect as e:
        return dict(error=str(e)), 401
    except UserInactive as e:
        return dict(error=str(e)), 401
    except Exception as e:
        return dict(error=str(e)), 500