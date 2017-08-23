from datetime import datetime
from neomodel.cardinality import One
from neomodel.properties import StringProperty, IntegerProperty, DateProperty, FloatProperty
from neomodel.relationship_manager import RelationshipFrom

from base.base_model import BaseModel
from exceptions.card_exception import NotEnoughCardArguments, UnchangeableCardValue, NotEnoughCardFreeLimit


class Card(BaseModel):
    number = StringProperty(required=True)
    due_day = IntegerProperty(required=True)
    expiration_date = DateProperty(required=True)
    cvv = StringProperty(required=True)
    max_limit = FloatProperty(required=True)
    free_limit_ = FloatProperty(required=True)

    wallet = RelationshipFrom('.wallet.Wallet', 'CONTAINED_BY', cardinality=One)

    def __init__(self, date_format='%m/%d/%Y', **kwargs):
        # Test if all arguments are present
        if not all(k in kwargs for k in ['number', 'due_day', 'expiration_date', 'cvv', 'max_limit']):
            raise NotEnoughCardArguments

        # set initial free_limit equals to max_limit
        kwargs['free_limit_'] = kwargs['max_limit']
        kwargs['cvv'] = str(kwargs['cvv'])

        # as discussed by e-mail, due_day is limited from 1 to 28
        if kwargs['due_day'] < 1 or kwargs['due_day'] > 28:
            raise ValueError('due_date should be limited from 1 to 28 to avoid problems with some months')

        if type(kwargs['expiration_date']) is str:
            kwargs['expiration_date'] = datetime.strptime(kwargs['expiration_date'], date_format).date()

        fake_today = kwargs['fake_today'] if 'fake_today' in kwargs else None
        date_format = kwargs['date_format'] if 'date_format' in kwargs else '%m/%d/%Y'

        super(Card, self).__init__(**kwargs)
        self.set_fake_today(fake_today, date_format)

    @property
    def due_date(self):
        """
        Returns next due date based on atual date and due_day
        """

        due_date = self.fake_today.replace(day=self.due_day)

        # due date is next month
        if self.due_day <= self.fake_today.day:
            year = due_date.year + due_date.month // 12
            month = due_date.month % 12 + 1
            due_date = due_date.replace(month=month, year=year)

        return due_date

    def set_fake_today(self, fake_today=None, date_format='%m/%d/%Y'):
        self.fake_today = fake_today if fake_today else datetime.today().date()

        if type(self.fake_today) is str:
            self.fake_today = datetime.strptime(fake_today, date_format).date()

        self.date_format = date_format

    @property
    def free_limit(self):
        return self.free_limit_

    @free_limit.setter
    def free_limit(self, value):
        """
        Raise exception: can't change free_limit directly
        :param value: value to be changed
        """
        raise UnchangeableCardValue()

    def decrease_free_limit(self, value):
        """
        Decrease free limit, used on purchasing
        :param value: value to reduce free_limit
        :return: new value for free_limit
        """
        # if there is not enough free_limit, raise exception
        if self.free_limit < value:
            raise NotEnoughCardFreeLimit()

        # if there is free limit, reduce value amount from it
        self.free_limit_ = self.free_limit_ - value
        self.save()
        return self.free_limit

    def purchase(self, value):
        """
        Test if there is enough free limit, then
        reduce free_limit by value
        :param value: purchase value
        """
        self.decrease_free_limit(value)

    def __lt__(self, other):

        if self.due_date > other.due_date:
            return True
        elif self.due_date == other.due_date:
            return self.max_limit < other.max_limit
        else:
            return False
