import csv
import calendar
from io import StringIO
from datetime import datetime
from flask import Blueprint, abort, jsonify, make_response
from sqlalchemy import extract
from ..models import Customer, Subscription, StatusType


bp = Blueprint("customers", __name__, url_prefix="/customers")


@bp.route("/", strict_slashes=False, methods=["GET"])
def get_customer_list():
    customers = Customer.query.all()
    return jsonify({"customers": [customer.to_dict() for customer in customers]})


@bp.route("/<customer_id>", methods=["GET"])
def get_customer(customer_id):
    customer = Customer.query.filter_by(id=customer_id).first()
    if not customer:
        abort(404, {"code": 404, "message": "customer not found."})
    return jsonify(customer.to_dict())
