from neomodel.cardinality import One
from neomodel.properties import FloatProperty, DateTimeProperty
from neomodel.relationship import StructuredRel
from neomodel.relationship_manager import RelationshipTo, RelationshipFrom

from base.base_model import BaseModel
from exceptions.purchase_exceptions import PurchaseUnchangeableProperty

"""
This module contains classes used in purchase and payment
"""

# == Billing Action ===
class BillingAction(StructuredRel):
    """
    A relationship definition who related cards and Purchases,
    once the purchase may be done in more than a card, this class
    defines how much was payid in which card.
    """
    value = FloatProperty(required=True)
    date_time = DateTimeProperty(default_now=True)

# === Purchase ===
class Purchase(BaseModel):
    """
    Purchase objects represents a purchase made with wallet,
    it is, with one or more cards
    """
    total = FloatProperty(required=True)

    cards_ = RelationshipTo('.card.Card', 'WITH', model=BillingAction)
    wallet_ = RelationshipFrom('.wallet.Wallet', 'DONE_WITH', cardinality=One)

    @property
    def wallet(self):
        return self.wallet_

    @wallet.setter
    def wallet(self, wallet):
        raise PurchaseUnchangeableProperty()

    @property
    def cards(self):
        return self.cards_

    @cards.setter
    def cards(self, card):
        raise PurchaseUnchangeableProperty()

    def use_card(self, card, value):
        self.cards_.connect(card, {'value': value})
        self.save()
        card.purchases.connect(self, {'value': value})

        card.decrease_free_limit(value)
        card.save()

        return self

    def to_dict(self):
        card_relations = []

        for card in self.cards:
            relation = dict()
            relation['cid'] = card.uid

            rel = self.cards.relationship(card)
            relation['value'] = rel.value
            relation['date_time'] = rel.date_time

            card_relations.append(relation)

        return dict(wid=self.wallet.single().uid,
                    total=self.total,
                    relations=relation)

    def set_wallet(self, wallet):
        self.save()
        self.wallet_.connect(wallet)
        wallet.purchases.connect(self)
        self.save()
        wallet.save()

        return self


# === Payment ===
class Payment(BaseModel):
    """
    Payment object represents a payment for a card
    contained in a wallet
    """
    value = FloatProperty()
    date_time = DateTimeProperty(default_now=True)
    card = RelationshipTo('.card.Card', 'FOR', cardinality=One)
    wallet = RelationshipFrom('.wallet.Wallet', 'FOR', cardinality=One)

    def to_dict(self):
        return dict(value=self.value,
                    cid=self.card.single().uid,
                    date_time=self.date_time,
                    wid=self.wallet.single().uid)
