from neomodel.cardinality import One
from neomodel.properties import FloatProperty, DateTimeProperty
from neomodel.relationship import StructuredRel
from neomodel.relationship_manager import RelationshipTo, RelationshipFrom

from base.base_model import BaseModel
from exceptions.purchase_exceptions import PurchaseUnchangeableProperty

class BillingAction(StructuredRel):
    value = FloatProperty(required=True)
    date_time = DateTimeProperty(default_now=True)

class Purchase(BaseModel):
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

    def set_wallet(self, wallet):
        self.save()
        self.wallet_.connect(wallet)
        wallet.purchases.connect(self)
        self.save()
        wallet.save()

        return self


class Payment(BaseModel):
    value = FloatProperty()
    card = RelationshipTo('.card.Card', 'FOR', cardinality=One)
    wallet = RelationshipFrom('.wallet.Wallet', 'FOR', cardinality=One)
