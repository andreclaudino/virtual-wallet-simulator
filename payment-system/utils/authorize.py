from functools import wraps

import os
from flask import request
from itsdangerous import TimedJSONWebSignatureSerializer, SignatureExpired, BadSignature

"""
This module contains functions useful for authorization
and basic server configuration
"""

def server_config():
    """
    Function to get server configuration from
    file (server_config.json), or return defaults
    (best suited for development) if file not
    found

    Have the following fields:

    *  run_config: dictionary with configurations
    for flask app run

        *  port: http port to listen
        *  host: http host to listen
        *  debug: if should run in flask debug
        mode (optional, default=False)

    *  secret_key: secret key used to sign auth token
    *  expiration_time: time to live of auth token
    """

    return dict(secret_key=os.environ.get("SECRET_KEY"),
                expiration_time=int(os.environ.get("EXPIRATION_TIME")))

def generate_auth_token(user):
    """
    Generate a signed auth token with key and
    expiration time got from server_config()

    * :param user: user who logged in
    return: signed token containing
    uid (user uid), wid (wallet uid),
    and username
    """
    username = user.username
    uid = user.uid
    wid = user.wallet_uid()

    secret_key = server_config()['secret_key']
    expires = server_config()['expiration_time']
    serializer = TimedJSONWebSignatureSerializer(secret_key, expires_in=expires)

    return serializer.dumps([username, uid, wid])


def read_auth_token(token):
    """
    Decode a token and get username and uid

    *  :param token: auth_token
    *  :return: username, user uid, wallet uid
    *  :raise:

        * SignatureExpired: token is valid, but expired
        * BadSignature: token is not valid
    """
    secret_key = server_config()['secret_key']
    expires = server_config()['expiration_time']
    serializer = TimedJSONWebSignatureSerializer(secret_key, expires_in=expires)
    return serializer.loads(token)


def verify_token(token):
    """
    Function which returns True if token
    is true and valid, else returns False

    *  :param token:
    *  :return: Boolean
    """
    try:
        if read_auth_token(token):
            return True
        else:
            return False
    except:
        return False


def authenticated(f):
    """
    Decorator to secure endpoints:
    evaluate token, if valid, give it
    contents to function (username, uid,
    and wid), else, return 401
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        # get token, if exist
        token = request.headers.get('token')

        # if token is falsy, return error
        if not token:
            return dict(error="No token given"), 401
        try:

            token = request.headers['token']
            username, uid, wid = read_auth_token(token)

            # Wrap contents of token in a dict and pass to function
            contents = dict(username=username, uid=uid, wid=wid)
            return f(contents=contents, *args, **kwargs)

        except SignatureExpired as e:
            return dict(error=str(e)), 401
        except BadSignature as e:
            return dict(error=str(e)), 401
        except Exception as e:
            return dict(error=str(e)), 500

    return decorated
