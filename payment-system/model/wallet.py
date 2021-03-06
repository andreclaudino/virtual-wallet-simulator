from neomodel.cardinality import One
from neomodel.properties import FloatProperty, StringProperty
from neomodel.relationship_manager import RelationshipTo, RelationshipFrom

from base.base_model import BaseModel
from exceptions.wallet_exceptions import WalletLimitExceed, RealLimitExceeded
from exceptions.wallet_exceptions import UnchangeableWalletValue
from exceptions.wallet_exceptions import WalletLimitNotAllowed
from model.billing import Purchase
from model.card import Card

# === wallet model ===
"""
This module contains wallet model class
"""

class Wallet(BaseModel):
    """
    Model a wallet in database
    """

    label = StringProperty(required=True)
    max_limit_ = FloatProperty(db_property='max_limit', default=0)
    real_limit_ = FloatProperty(db_property='real_limit', default=0)
    free_limit_ = FloatProperty(db_property='free_limit', default=0)

    owner = RelationshipFrom('.user.User', 'OWNED', cardinality=One)
    cards = RelationshipTo('.card.Card', 'CONTAINS')

    purchases = RelationshipTo('.billing.Purchase', 'DID')
    payments = RelationshipFrom('.billing.Payment', 'RECEIVED')

    # === real_limit ===
    @property
    def real_limit(self):
        """
        real_limit is set to max_limit by default
        """
        return self.real_limit_ if self.real_limit_ else self.max_limit

    @real_limit.setter
    def real_limit(self, value):
        """
        Wallet limit set by user. Should be
        less than max_limit and non-negative
        :param value: new real limit
        :return:
        """
        if value > self.max_limit:
            raise WalletLimitExceed()
        elif value < 0:
            raise WalletLimitNotAllowed()
        else:
            self.real_limit_ = value
        self.save()

    # === max_limit ===
    @property
    def max_limit(self):
        return self.max_limit_

    @max_limit.setter
    def max_limit(self, value):
        raise UnchangeableWalletValue()

    # === free_limit ===
    @property
    def free_limit(self):
        """
        usable remaining limit related to max_limit
        """
        return self.free_limit_

    @free_limit.setter
    def free_limit(self, value):
        raise UnchangeableWalletValue()

    # === real_free_limit ===
    @property
    def real_free_limit(self):
        """
        Analogous to free limit, but related to
        real_limit instead of max_limit
        :return:
        """
        return self.real_limit - self.total_used

    # === total_used ===
    @property
    def total_used(self):
        return self.max_limit - self.free_limit

    # === Limits Manipulators ===
    def increase_free_limit(self, value=1.0):
        """
        Increase free_limit of wallet, usually
        in card bill payments.
        :param value: amount to be increased
        :return: new free limit
        """
        self.free_limit_ += value
        self.save()
        return self.free_limit

    def decrease_free_limit(self, value=1.0):
        """
        Decrease free_limit of wallet, usually
        in purchases
        Raises an exception if limit become negative
        :param value: amount to reduce
        :return: new limit
        """
        if self.free_limit < value:
            raise WalletLimitNotAllowed()
        else:
            return self.increase_free_limit(-value)

    def increase_max_limit(self, amount=1.0):
        self.max_limit_ += amount
        self.save()
        return self.max_limit

    def decrease_max_limit(self, amount=1.0):

        # Raise exception if limit become negative
        if amount > self.max_limit:
            raise WalletLimitNotAllowed()

        self.max_limit_ -= amount
        self.save()

        if self.real_limit > self.max_limit:
            self.real_limit = self.max_limit

        return self.max_limit

    # === Card manipulators ===
    def create_card(self, **kwargs):
        card = Card(**kwargs)
        card.save()
        card.wallet.connect(self)

        self.cards.connect(card)

        self.increase_max_limit(card.max_limit)
        self.increase_free_limit(card.free_limit)

        self.save()
        card.save()

        return card

    def sorted_cards(self, fake_today=None, date_format='%m/%d/%Y'):
        """
        Sort cards by distance to due date, than to lower limit
        considering today as fake_today
        :param fake_today: a pseudo date (or None for today)
        :param date_format: (format of used date)
        :return: active cards sorted according to rules in
        (enuntiate)[https://slack-files.com/T06M9ENDT-F5XK4J0P2-532510c5c0]
        """
        cards = []

        for card in self.cards:
            if card.active:
                card.set_fake_today(fake_today, date_format)
                cards.append(card)

        cards.sort()
        return cards

    # === object dictionarization ===
    def to_dict(self):
        return dict(real_limit=self.real_limit,
                    max_limit=self.max_limit,
                    free_limit=self.free_limit,
                    real_free_limit=self.real_free_limit,
                    total_used=self.total_used,
                    total_cards=len(self.cards))

    # === purchase ===
    def purchase(self, value):
        """
        Purchase following rules in
        (enuntiate)[https://slack-files.com/T06M9ENDT-F5XK4J0P2-532510c5c0]
        :param value:
        :return: Purchase object generated on purchase
        """
        # Raise RealLimitExceeded if purchase exceeds real_free_limit
        if self.real_free_limit < value:
            raise RealLimitExceeded()

        purchase = Purchase()
        purchase.total = value
        purchase = purchase.set_wallet(self)

        # If possible, purchase with only one card
        for card in self.sorted_cards():
            if card.free_limit >= value:
                purchase = purchase.use_card(card, value)
                return purchase

        # Else, purchase with multiple cards
        for card in self.sorted_cards():

            value_in_card = value if card.free_limit > value else card.free_limit

            purchase = purchase.use_card(card, value_in_card)
            value -= value_in_card

            if value <= 0:
                break

        return purchase