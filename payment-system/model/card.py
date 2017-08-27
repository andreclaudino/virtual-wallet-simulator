import warnings
from datetime import datetime
from neomodel.cardinality import One
from neomodel.properties import StringProperty, IntegerProperty, DateProperty, FloatProperty
from neomodel.relationship_manager import RelationshipFrom

from base.base_model import BaseModel
from exceptions.card_exceptions import NotEnoughCardArguments, CardAlreadyActive, CardAlreadyInactive, CardIsInactive
from exceptions.card_exceptions import UnchangeableCardValue
from exceptions.card_exceptions import NotEnoughCardFreeLimit
from exceptions.card_exceptions import PaymentExceed
from model.billing import BillingAction


class Card(BaseModel):
    number = StringProperty(required=True)
    due_day = IntegerProperty(required=True)
    expiration_date = DateProperty(required=True)
    cvv = StringProperty(required=True)
    max_limit = FloatProperty(required=True)
    free_limit_ = FloatProperty(required=True)

    wallet = RelationshipFrom('.wallet.Wallet', 'CONTAINED_BY', cardinality=One)
    purchases = RelationshipFrom('.billing.Purchase', 'DID', model=BillingAction)
    payments = RelationshipFrom('.billing.Payment', 'RECEIVED', model=BillingAction)

    def __init__(self, date_format='%m/%d/%Y', **kwargs):
        # Test if all arguments are present
        if not all(k in kwargs for k in ['number', 'due_day', 'expiration_date', 'cvv', 'max_limit']):
            raise NotEnoughCardArguments

        # set initial free_limit equals to max_limit
        kwargs['free_limit_'] = kwargs['free_limit_'] if 'free_limit_' in kwargs else kwargs['max_limit']

        kwargs['cvv'] = str(kwargs['cvv'])

        # as discussed by e-mail, due_day is limited from 1 to 28
        if kwargs['due_day'] < 1 or kwargs['due_day'] > 28:
            raise ValueError('due_date should be limited from 1 to 28 to avoid problems with some months')

        if type(kwargs['expiration_date']) is str:
            kwargs['expiration_date'] = datetime.strptime(kwargs['expiration_date'], date_format).date()

        fake_today = kwargs['fake_today'] if 'fake_today' in kwargs else None
        date_format = kwargs['date_format'] if 'date_format' in kwargs else '%m/%d/%Y'

        super(Card, self).__init__(**kwargs)

        self.date_format = '%m/%d/%Y'
        self.fake_today = None

        self.set_fake_today(fake_today, date_format)

    @property
    def due_date(self):
        """
        Calculate next due date based on atual date and due_day
        :return: next due date
        """
        due_date = self.get_fake_today().replace(day=self.due_day)

        # due date is next month
        if self.due_day <= self.fake_today.day:
            year = due_date.year + due_date.month // 12
            month = due_date.month % 12 + 1
            due_date = due_date.replace(month=month, year=year)

        return due_date

    def set_fake_today(self, fake_today=None, date_format='%m/%d/%Y'):
        """
        Assume a fake today date, set for today if None. Useful for tests
        and generate reference cards sortings
        :param fake_today: date or string representing date to be assumed for today
        :param date_format: format for parsing date when fake_today is string
        :return:
        """
        self.fake_today = fake_today if fake_today else datetime.today().date()

        if type(self.fake_today) is str:
            self.fake_today = datetime.strptime(fake_today, date_format).date()

        self.date_format = date_format

    def get_fake_today(self):
        return self.fake_today if self.fake_today else datetime.today().date()

    @property
    def free_limit(self):
        """
        Just get free_limit_
        :return: free_limit
        """
        return self.free_limit_

    @free_limit.setter
    def free_limit(self, value):
        """
        Just to avoid changing free_limit_ directly,
        it should be increased or decreased on
        each payment
        :param value: value to be changed
        """
        raise UnchangeableCardValue()

    @property
    def active(self):
        """
        A card should be inactive if it's set to be inactive, or
        if reached expiration date
        :return:
        """
        if self.expiration_date < self.fake_today:
            return False
        return self.active_

    @active.setter
    def active(self, state):
        """
        Change active state from an user.
        Raise warning if state is not changed
        :param state:
        :return:
        """

        if self.active and state:
            # raise warning if activating an already active card
            warnings.warn(CardAlreadyActive())
        elif (not self.active) and (not state):
            # raise warning if deactivating an already inactive card
            warnings.warn(CardAlreadyInactive())
        else:
            # Otherwise, process limits
            self.active_ = state
            if state:
                # increase wallet limits if activating the card
                self.wallet[0].increase_max_limit(self.max_limit)
                self.wallet[0].increase_free_limit(self.max_limit)
            else:
                # decrease wallet limit if deactivating the card
                self.wallet[0].decrease_max_limit(self.max_limit)
                self.wallet[0].decrease_free_limit(self.max_limit)
            self.save()

    def decrease_free_limit(self, value):
        """
        Decrease free limit, used on purchasing.
        raise NotEnoughCardFreeLimit if free_limit is
        not enough
        :param value: value to reduce free_limit
        :return: new value for free_limit
        """
        # if there is not enough free_limit, raise exception
        if self.free_limit < value:
            raise NotEnoughCardFreeLimit()

        # if there is free limit, reduce value amount from it
        self.free_limit_ -= value
        self.save()

        self.wallet.single().decrease_free_limit(value)
        self.wallet.single().refresh()

        return self.free_limit

    def increase_free_limit(self, value):
        """
        Increase free limit, used on payment.
        raises PaymentExceed when payment value
        and free_limit exceed maximum card limit
        :param value: value to increase free_limit
        :return: new value for free_limit
        """

        # raise exception if exceed maximum limit of card
        if self.free_limit + value > self.max_limit:
            raise PaymentExceed

        # if no problem, increase limit
        self.free_limit_ = self.free_limit_ + value
        self.save()

        self.wallet[0].increase_free_limit(value)
        self.wallet[0].refresh()

        return self.free_limit

    def purchase(self, value):
        """
        Process a purchase,
        raise CardIsInactive if card is inactive
        :param value: purchase value
        """

        if not self.active:
            raise CardIsInactive()

        self.decrease_free_limit(value)

    def pay(self, value):
        """
        Release credit increasing free_limit. Raise PaymentExceed if
        value+free_limit exceeds max_limit
        :param value: payed amount
        :return: new free_limit
        """
        self.increase_free_limit(value)

    def __lt__(self, other):
        """
        Order cards, first by largest due date,
        then by smaller maxmimum limit
        :param other: other object which is beeing compared
        :return: True if is lower, False if is bigger than other
        """
        if self.due_date > other.due_date:
            return True
        elif self.due_date == other.due_date:
            return self.max_limit < other.max_limit
        else:
            return False

    def __str__(self):
        s = '<Card[limit: {max_limit}, due_day: {due_date}, expiration: {expiration}, cvv: {cvv}]>'
        return s.format(max_limit=self.max_limit,
                        due_date=self.due_date,
                        expiration=self.due_date,
                        cvv=self.cvv)