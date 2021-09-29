import os
import logging

from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.logger.setLevel(logging.INFO)
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI="sqlite:///"
        + os.path.join(app.instance_path, "billing.sqlite"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config is None:
        # load the instance config, if it exists
        app.config.from_pyfile("application.cfg", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # init database
    from .database import init_db
    init_db(app)

    # init endpoints
    from .views import customers, invoices
    app.register_blueprint(customers.bp)
    app.register_blueprint(invoices.bp)

    @app.errorhandler(Exception)
    def handle_exception(error):
        # handling HTTP errors
        if isinstance(error, HTTPException):
            return (
                jsonify({"error": {"code": error.code, "message": error.description}}),
                error.code,
            )

        # handling non-HTTP erros only
        return jsonify({"error": {"code": 500, "message": "Server error."}}), 500

    return app
