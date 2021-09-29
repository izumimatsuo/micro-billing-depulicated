from flask import Blueprint, abort, jsonify
from ..models import Plan


app = Blueprint("plans", __name__)


@app.route("/plans", strict_slashes=False, methods=["GET"])
def get_plan_list():
    plans = Plan.query.all()
    return jsonify({"plans": [plan.to_dict() for plan in plans]})


@app.route("/plans/<plan_id>", methods=["GET"])
def get_plan(plan_id):
    plan = Plan.query.filter_by(id=plan_id).first()
    if not plan:
        abort(404, {"code": 404, "message": "plan not found."})
    return jsonify(plan.to_dict())
