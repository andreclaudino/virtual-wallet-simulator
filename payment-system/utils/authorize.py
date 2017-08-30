from functools import wraps

from flask import json
from flask import request
from itsdangerous import TimedJSONWebSignatureSerializer, SignatureExpired, BadSignature


def server_config():
    """
    Function to get server configuration from
    file (server_config.json), or return defaults
    (best suited for development)
    :return: dictionary with configurations
    """
    defaults = {
                'run_config': {
                    'port': 8080,
                    'host': '0.0.0.0',
                    'debug': True
                },
                'secret_key': '0000000000000',
                'expiration_time': 3600
               }

    # load server configuration
    try:
        with open('server_config.json') as f:
            return json.load(f)
    except FileNotFoundError as e:
        # if file not found, return defaults and raise warn
        return defaults
    except ValueError as e:
        # if file found, but has problem in parse, raise exception
        print("Error parsing 'server_config.json': {}".format(e))

def generate_auth_token(user):

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
    :param token: auth_token
    :return: username, user uid, wallet uid
    :raise:
        * SignatureExpired: token is valid, but expired
        * BadSignature: token is not valid
    """
    secret_key = server_config()['secret_key']
    expires = server_config()['expiration_time']
    serializer = TimedJSONWebSignatureSerializer(secret_key, expires_in=expires)
    return serializer.loads(token)


def verify_token(token):
    try:
        if read_auth_token(token):
            return True
        else:
            return False
    except:
        return False


def authenticated(f):
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
