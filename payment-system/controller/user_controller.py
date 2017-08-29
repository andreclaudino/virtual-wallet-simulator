from base.base_controller import BaseController
from exceptions.user_exceptions import UsernameInUse
from model.user import User
from flask import request

from utils.authorize import authenticated

user_blueprint = BaseController('user')


@user_blueprint.route('', methods=['POST'])
def create():

    form = request.values

    try:
        user = User(name=form['name'],
                    username=form['username'],
                    adress=form['adress'],
                    phone_number=form['phone_number'],
                    mail_address=form['mail_address'],
                    password=form['password'])
        user.save()
        user.refresh()

        user.create_wallet("Wallet of {}".format(user.name))
        user.save()

        user.refresh()

        return user.to_dict(), 201

    except UsernameInUse as e:
        return dict(error=str(e)), 409

    except Exception as e:
        return dict(error=str(e)), 500

@user_blueprint.route('/<uid>', methods=['GET'])
@authenticated
def get(uid, contents=None):

    user = User.nodes.get_or_none(uid=uid)

    if user:
        return user.to_dict()
    else:
        return dict(error='User not found'), 404

@user_blueprint.route('/username/<username>', methods=['GET'])
@authenticated
def get_by_username(username, contents=None):
    user = User.nodes.get_or_none(username=username)

    if user:
        return user.to_dict()
    else:
        return dict(error='User not found'), 404

