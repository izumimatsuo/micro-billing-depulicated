import csv
import calendar
from io import StringIO
from datetime import datetime
from flask import Blueprint, abort, jsonify, make_response
from ..models import Subscription


app = Blueprint("subscriptions", __name__)


@app.route("/subscriptions", strict_slashes=False, methods=["GET"])
def get_subscription_list():
    subscriptions = Subscription.query.all()
    return jsonify({"subscriptions": [subscription.to_dict() for subscription in subscriptions]})


@app.route("/subscriptions/<subscription_id>", methods=["GET"])
def get_subscription(subscription_id):
    subscription = Subscription.query.filter_by(id=subscription_id).first()
    if not subscription:
        abort(404, {"code": 404, "message": "subscription not found."})
    return jsonify(subscription.to_dict())
