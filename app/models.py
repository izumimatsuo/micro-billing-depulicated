import enum
from datetime import datetime
from .database import db


# ISO 4217
class CurrencyType(str, enum.Enum):
    jpy = "jpy"
    usd = "usd"


class StatusType(str, enum.Enum):
    active = "active"  # 有効
    past_due = "past_due"  # 遅延
    unpaid = "unpaid"  # 未払い
    canceled = "canceled"  # 解約
    incomplete = "incomplete"  # 不完全
    incomplete_expired = "incomplete_expired"  # 有効期限切れ
    trialing = "trialing"  # 試用


class Plan(db.Model):
    __tablename__ = "plans"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    currency = db.Column(db.Enum(CurrencyType), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now
    )

    def __init__(self, id, name, amount, currency):
        self.id = id
        self.name = name
        self.amount = amount
        self.currency = currency

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            amount=self.amount,
            currency=self.currency
        )


class Customer(db.Model):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now
    )

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name,
        )


class Subscription(db.Model):
    __tablename__ = "subscriptions"

    id = db.Column(db.Integer, primary_key=True)
    current_period_start = db.Column(db.DateTime, nullable=False)
    current_period_end = db.Column(db.DateTime, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)
    customer = db.relationship(Customer, backref="customers")
    plan_id = db.Column(db.Integer, db.ForeignKey("plans.id"), nullable=False)
    plan = db.relationship(Plan, backref="plans")
    status = db.Column(db.Enum(StatusType), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now
    )

    def __init__(self, id, current_period_start, current_period_end, customer_id, plan_id, status, start_date):
        self.id = id
        self.current_period_start = current_period_start
        self.current_period_end = current_period_end
        self.customer_id = customer_id
        self.plan_id = plan_id
        self.status = status
        self.start_date = start_date

    def to_dict(self):
        return dict(
            id=self.id,
            current_period_start=str(self.current_period_start),
            current_period_end=str(self.current_period_end),
            customer_id=self.customer_id,
            plan_id=self.plan_id,
            status=self.status,
            start_date=str(self.start_date)
        )
