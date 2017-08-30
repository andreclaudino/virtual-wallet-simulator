from flask.globals import request
from neomodel.exception import DoesNotExist

from base.base_controller import BaseController
from exceptions.card_exceptions import NotEnoughCardArguments, PaymentExceed
from exceptions.wallet_exceptions import WalletLimitExceed, WalletLimitNotAllowed, RealLimitExceeded
from model.card import Card
from model.wallet import Wallet
from utils.authorize import authenticated

# === Wallet route module ===
"""
Endpoints to get information about wallet and cards,
purchas, manage wallet limits and cards and pay card

All endpoints in here are secured, i.e. they need
a valid token
"""

wallet_blueprint = BaseController('wallet')


# === GET /wallet ===
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


# === PUT /wallet/real_limit ===
@wallet_blueprint.route('/real_limit', methods=['PUT'])
@wallet_blueprint.route('/real_limit/<float:value>', methods=['PUT'])
@authenticated
def set_real_limit(value=None, contents=None):
    """
    Change real limit (user defined maximum limit) of a wallet
    Returns:

         * 406 if maximum limit was exceed
         * 406 if free limit become negative
    """
    try:
        value = value if value else request.values['value']

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


# === POST /wallet/cards ===
@wallet_blueprint.route('/cards', methods=['POST'])
@authenticated
def create_card(contents=None):
    """
    Add a card to the wallet.
    Returns:
        * 406 if there is not all necessary card arguments
    """
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


# === DELETE /wallet/cards/cid ===
@wallet_blueprint.route('/cards', methods=['DELETE'])
@wallet_blueprint.route('/cards/<cid>', methods=['DELETE'])
@authenticated
def deactivate_card(cid=None, contents=None):
    """
    Deactivate a card, i.e. same as delete,
    it become unuseful for wallet, but is still
    able to receive payments until reach maximum
    payment limit, it is, until free_limit become
    max_limit
    """
    try:
        cid = cid if cid else request.values['cid']
        card = Card.nodes.get(uid=cid)
        card.active = False
        card.save()

        card.refresh()

        return card.to_dict()

    except DoesNotExist as e:
        return dict(error=str(e)), 404
    except Exception as e:
        return dict(error=str(e)), 500


# === GET /wallet/cards ===
@wallet_blueprint.route('/cards', methods=['GET'])
@authenticated
def get_cards(contents=None):
    """
    Get cards related to token's wallet
    """
    try:
        wallet = Wallet.nodes.get(uid=contents['wid'])
        cards = [card.to_dict() for card in wallet.cards]

        return dict(wid=wallet.uid, cards=cards)
    except Exception as e:
        return dict(error=str(e)), 500


# === GET /wallet/cards/sorted ===
@wallet_blueprint.route('/cards/sorted', methods=['GET'])
@authenticated
def get_sorted_cards(contents=None):
    """
    Get active cards related to token's
    wallet sorted in order of precedence
    for purchase
    """
    try:
        wallet = Wallet.nodes.get(uid=contents['wid'])
        cards = [card.to_dict() for card in wallet.sorted_cards()]

        return dict(wid=wallet.uid, cards=cards)
    except Exception as e:
        return dict(error=str(e)), 500


# === GET /wallet/cards/<cid> ===
@wallet_blueprint.route('/cards/<cid>', methods=['GET'])
@authenticated
def get_card(cid=None, contents=None):
    """
    Get a card with uid = cid
    Returns:

        * 404 if card is not found
    """
    try:
        card = Card.nodes.get(uid=cid)
        return card.to_dict()

    except DoesNotExist as e:
        return dict(error=str(e)), 404
    except Exception as e:
        return dict(error=str(e)), 500


# === POST /wallet/purchase ===
@wallet_blueprint.route('/purchase', methods=['POST'])
@wallet_blueprint.route('/purchase/<float:value>', methods=['POST'])
@authenticated
def purchase(value=None, contents=None):
    """
    Do a purchase token's wallet
    Returns:

        * 406 if wallet limit will be exceed
        by this purchase
        * 406 if wallet limit is less than
        the needed for purchase
    """
    try:
        value = value if value else request.values['value']
        wallet = Wallet.nodes.get(uid=contents['wid'])
        purchase_obj = wallet.purchase(float(value))
        return purchase_obj.to_dict()

    except DoesNotExist as e:
        return dict(error=str(e)), 404
    except RealLimitExceeded as e:
        return dict(error=str(e)), 406
    except WalletLimitNotAllowed as e:
        return dict(error=str(e)), 406
    except Exception as e:
        return dict(error=str(e)), 500


# === POST /wallet/cards/<cid>/pay ===
@wallet_blueprint.route('/cards/pay', methods=['POST'])
@wallet_blueprint.route('/cards/<cid>/pay', methods=['POST'])
@authenticated
def pay_card(cid=None, contents=None):
    """
    Relase credit of a card identified by uid=cid
    Require cid and value (amount to be payed)
    Returns:

        * 404 if card don't exist
        * 406 if free_limit + value
        exceed maximum card limit
    """
    try:
        cid = cid if cid else request.values['cid']
        value = float(request.values['value'])

        card = Card.nodes.get(uid=cid)
        pay_object = card.pay(value)
        return pay_object.to_dict()

    except DoesNotExist as e:
        return dict(error=str(e)), 404
    except PaymentExceed as e:
        return dict(error=str(e)), 406
    except Exception as e:
        return dict(error=str(e)), 500

