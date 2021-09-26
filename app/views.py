import csv
from io import StringIO
from flask import Blueprint, abort, jsonify, make_response
from .models import Customer


bp = Blueprint("default", __name__, url_prefix="/")


@bp.route("/customers", methods=["GET"])
def get_customer_list():
    customers = Customer.query.all()
    return jsonify({"customers": [customer.to_dict() for customer in customers]})


@bp.route("/customers/<customer_id>", methods=["GET"])
def get_customer(customer_id):
    customer = Customer.query.filter_by(id=customer_id).first()
    if not customer:
        abort(404, {"code": 404, "message": "customer not found."})
    return jsonify(customer.to_dict())


@bp.route("/invoices", methods=["GET"])
def create_invoices():
    f = StringIO()
    writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)

    writer.writerow(["name", "amount"])
    for c in Customer.query.filter_by(active=True).all():
        writer.writerow([c.name, c.amount])

    res = make_response()
    res.data = f.getvalue()
    res.headers["Content-Type"] = "text/csv"
    #    res.headers['Content-Disposition'] = 'attachment; filename='+ obj +'.csv'
    return res
