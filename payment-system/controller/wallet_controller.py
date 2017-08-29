from flask.globals import request
from neomodel.exception import DoesNotExist

from base.base_controller import BaseController
from exceptions.card_exceptions import NotEnoughCardArguments
from exceptions.wallet_exceptions import WalletLimitExceed, WalletLimitNotAllowed
from model.card import Card
from model.wallet import Wallet
from utils.authorize import authenticated

wallet_blueprint = BaseController('wallet')

@wallet_blueprint.route('', methods=['GET'])
@authenticated
def get_wallet_info(contents=None):
    """
    Return wallet basic information
    """
    try:
        wallet = Wallet.nodes.get_or_none(uid=contents['wid'])
    except Exception as e:
        return dict(error=str(e)), 500

    return wallet.to_dict()

@wallet_blueprint.route('/real_limit/<float:value>', methods=['PUT'])
@authenticated
def set_real_limit(value=None, contents=None):
    try:
        wallet = Wallet.nodes.get(uid=contents['wid'])
        wallet.real_limit = float(value)
        wallet.refresh()
        return wallet.to_dict()

    except WalletLimitExceed as e:
        return dict(error=str(e)), 406
    except WalletLimitNotAllowed as e:
        return dict(error=str(e)), 406
    except DoesNotExist as e:
        return dict(error=str(e)), 404
    except Exception as e:
        return dict(error=str(e)), 500

@wallet_blueprint.route('/cards', methods=['POST'])
@authenticated
def create_card(contents=None):
    try:
        args = request.values
        wallet = Wallet.nodes.get(uid=contents['wid'])

        card = wallet.create_card(number=args['number'],
                                  due_day=int(args['due_day']),
                                  expiration_date=args['expiration_date'],
                                  cvv=args['cvv'],
                                  max_limit=float(args['max_limit']))

        wallet.save()
        return card.to_dict()
    except NotEnoughCardArguments as e:
        return dict(error=str(e)), 406
    except Exception as e:
        return dict(error=str(e)), 500

@wallet_blueprint.route('/cards/<cid>', methods=['DELETE'])
@authenticated
def deactivate_card(cid=None, contents=None):
    """
    Deactivate a card
    """
    try:
        card = Card.nodes.get(uid=cid)
        card.active = False
        card.save()

        card.refresh()

        return card.to_dict()

    except DoesNotExist as e:
        return dict(error=str(e)), 404
    except Exception as e:
        return dict(error=str(e)), 500

@wallet_blueprint.route('/cards', methods=['GET'])
@authenticated
def get_cards(contents=None):
    try:
        wallet = Wallet.nodes.get(uid=contents['wid'])
        cards = [card.to_dict() for card in wallet.cards]

        return dict(wid=wallet.uid, cards=cards)
    except Exception as e:
        return dict(error=str(e)), 500

@wallet_blueprint.route('/cards/<cid>', methods=['GET'])
@authenticated
def get_card(cid=None, contents=None):
    """
    Get a card
    """
    try:
        card = Card.nodes.get(uid=cid)
        return card.to_dict()

    except DoesNotExist as e:
        return dict(error=str(e)), 404
    except Exception as e:
        return dict(error=str(e)), 500


@wallet_blueprint.route('/cards/<cid>/pay/<float:value>', methods=['PUT'])
@authenticated
def purchase(value=None, contents=None):
    """
    Do a purchase in wallet
    """


@wallet_blueprint.route('/cards/<cid>/pay/<float:value>', methods=['PUT'])
@authenticated
def pay_card(cid=None, value=None, contents=None):
    """
    Pay an amount in a card
    """
    pass

# NOTE: low-priority
@wallet_blueprint.route('/events/<since>/<until>', methods=['GET'])
@authenticated
def events(since=None, until=None, cid=None, contents=None):
    pass