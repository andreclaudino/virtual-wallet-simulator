from flask import request
from itsdangerous import SignatureExpired
from itsdangerous import BadSignature

from base.base_controller import BaseController
from exceptions.user_exceptions import UsernameNotFound
from exceptions.user_exceptions import UserPasswordIncorrect
from exceptions.user_exceptions import UserInactive
from model.user import User
from utils.authorize import generate_auth_token
from utils.authorize import read_auth_token

# === Controller for root endpoint ===
"""
RootController is a blueprint to deal with root of server.
Used to modularize instead of routing directly in application
"""
root_blueprint = BaseController('root')

# === / ===
@root_blueprint.route('/')
def health_check():
    """
    Simple health check to evaluate if server
    is running properly
    """
    return dict(api_status='OK')

# === POST /login ===
@root_blueprint.route('/login', methods=['POST'])
def login():
    """
    Perform login and generate auth token
    for this session.
    Returns:

        * 401 for username not found
        * 401 for password incorrect
        * 401 for user marked as inactive
    """
    try:
        form = request.values

        username = form['username']
        password = form['password']

        user = User.login(username, password)
        token = generate_auth_token(user)

        return dict(user=user.to_dict(), token=token.decode('ascii'))

    except UsernameNotFound as e:
        return dict(error=str(e)), 401
    except UserPasswordIncorrect as e:
        return dict(error=str(e)), 401
    except UserInactive as e:
        return dict(error=str(e)), 401
    except Exception as e:
        return dict(error=str(e)), 500

# === GET /whoami ===
@root_blueprint.route('/whoami', methods=['GET'])
def whoami():
    """
    Simple endpoint to get information from
    auth_token.

    Returns:

        * 401 for expired token
        * 401 for false token
    """
    try:

        token = request.headers['token']
        username, uid, wid = read_auth_token(token)
        return dict(username=username, uid=uid, wid=wid)

    except SignatureExpired as e:
        return dict(error=str(e)), 401
    except BadSignature as e:
        return dict(error=str(e)), 401
    except Exception as e:
        return dict(error=str(e)), 500
