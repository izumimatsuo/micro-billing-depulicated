import enum
from datetime import datetime
from .database import db


# ISO 4217
class CurrencyType(str, enum.Enum):
    jpy = "jpy"
    usd = "usd"


# class Plan(db.Model):
#    __tablename__ = 'plans'
#    id = db.Column(db.Integer, primary_key = True)
#    name = db.Column(db.String, nullable = False)
#    amount = db.Column(db.Integer, nullable = False)
#    currency = db.Column(db.Enum(CurrencyType), nullable = False)
#
#    def __init__(self,):
#
#    def to_dict(self):
#        return dict(
#       )
#
#    def __repr__(self):
#        return '<Plan {}>'.format(self.nickname)


class Customer(db.Model):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now
    )

    def __init__(self, id, name, active, amount, start_date):
        self.id = id
        self.name = name
        self.active = active
        self.amount = amount
        self.start_date = start_date

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            active=self.active,
            amount=self.amount,
            start_date=self.start_date,
        )

    def __repr__(self):
        return "<Customer {}>".format(self.name)
