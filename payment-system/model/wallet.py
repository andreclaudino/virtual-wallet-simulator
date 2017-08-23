from neomodel.cardinality import One
from neomodel.properties import FloatProperty, StringProperty
from neomodel.relationship_manager import RelationshipTo, RelationshipFrom

from datetime import datetime

from base.base_model import BaseModel
from exceptions.wallet_exceptions import WalletLimitExceed, UnchangeableWalletValue, WalletLimitNotAllowed, \
    WalletFreeLimitExceed
from model.card import Card


class Wallet(BaseModel):

    label = StringProperty(required=True)
    max_limit_ = FloatProperty(db_property='max_limit', default=0)
    real_limit_ = FloatProperty(db_property='real_limit', default=0)
    free_limit_ = FloatProperty(db_property='free_limit', default=0)

    owner = RelationshipFrom('.user.User', 'OWNED', cardinality=One)
    cards = RelationshipTo('.card.Card', 'CONTAINS')

    @property
    def real_limit(self):
        return self.real_limit_

    @real_limit.setter
    def real_limit(self, value):
        if value > self.max_limit:
            raise WalletLimitExceed()
        elif value < 0:
            raise WalletLimitNotAllowed
        else:
            self.real_limit_ = value

    @property
    def max_limit(self):
        return self.max_limit_

    @max_limit.setter
    def max_limit(self, value):
        raise UnchangeableWalletValue()

    @property
    def free_limit(self):
        return self.free_limit_

    @free_limit.setter
    def free_limit(self, value):
        raise UnchangeableWalletValue()

    def increase_free_limit(self, value=1.0):
        """
        Increase free_limit of wallet, usually
        in card bill payments.
        Raises an exception if new free_limit
        become negative
        :param value: amount to be increased
        :return: new free limit
        """
        if self.free_limit + value < 0:
            raise WalletLimitNotAllowed()
        else:
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
        return self.increase_free_limit(-value)

    def increase_max_limit(self, amount=1.0):
        self.max_limit_ += amount

    def decrease_max_limit(self, amount=1.0):

        # Raise exception if limit become negative
        if amount > self.max_limit:
            raise WalletLimitNotAllowed()

        self.increase_max_limit(-amount)

        if self.real_limit > self.max_limit:
            self.real_limit = self.max_limit

        return self.max_limit

    def create_card(self, **kwargs):
        card = Card(**kwargs)
        card.save()
        card.wallet.connect(self)

        self.cards.connect(card)
        self.save()
        card.save()

        return card

    def sorted_cards(self):
        cards = [card for card in self.cards if card.active]

        cards.sort()
        return cards

