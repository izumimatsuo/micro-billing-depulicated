import os

from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException
from .database import init_db
from .models import Customer
from .views import bp

# create and configure the app
app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY="dev",
    SQLALCHEMY_DATABASE_URI="sqlite:///"
    + os.path.join(app.instance_path, "billing.sqlite"),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

# load the instance config, if it exists
app.config.from_pyfile("application.cfg", silent=True)

# setting the endpoints
app.register_blueprint(bp)

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

init_db(app)

@app.errorhandler(Exception)
def handle_exception(error):
    # handling HTTP errors
    if isinstance(error, HTTPException):
        return jsonify({'error': {
            'code': error.code,
            'message': error.description
        }}), error.code

    # handling non-HTTP erros only
    return jsonify({'error': {
        'code': 500,
        'message': 'Server error.'
    }}), 500
