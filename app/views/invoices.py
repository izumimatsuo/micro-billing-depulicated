import csv
import calendar
from io import StringIO
from datetime import datetime
from flask import Blueprint, abort, make_response
from sqlalchemy import extract
from ..models import Subscription, StatusType


app = Blueprint("invoices", __name__)


@app.route("/invoices", strict_slashes=False, methods=["GET"])
def create_invoices():
    f = StringIO()
    writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)

    writer.writerow(["name", "amount", "start_date"])
    for t in Subscription.query.filter(Subscription.status == StatusType.active).all():
        writer.writerow([t.customer.name, t.plan.amount, t.start_date])

    res = make_response()
    res.data = f.getvalue()
    res.headers["Content-Type"] = "text/csv"
    #    res.headers['Content-Disposition'] = 'attachment; filename='+ obj +'.csv'
    return res


@app.route("/invoices/<invoice_date>", methods=["GET"])
def create_invoices_by_date(invoice_date):

    try:
        invoice_datetime = datetime.strptime(invoice_date, "%Y%m%d")
    except ValueError:
        abort(400, {"code": 400, "message": "bad qequest."})

    if (
        invoice_datetime.day
        == calendar.monthrange(invoice_datetime.year, invoice_datetime.month)[1]
    ):
        targets = Subscription.query.filter(
            Subscription.status == StatusType.active,
            extract("day", Subscription.start_date) >= invoice_datetime.day,
        ).all()
    else:
        targets = Subscription.query.filter(
            Subscription.status == StatusType.active,
            extract("day", Subscription.start_date) == invoice_datetime.day,
        ).all()

    f = StringIO()
    writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)

    writer.writerow(["name", "amount", "start_date"])
    for t in targets:
        writer.writerow([t.customer.name, t.plan.amount, t.start_date])

    res = make_response()
    res.data = f.getvalue()
    res.headers["Content-Type"] = "text/csv"
    #    res.headers['Content-Disposition'] = 'attachment; filename='+ obj +'.csv'
    return res
