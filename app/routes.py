import json

from flask import Blueprint, abort, current_app, jsonify, request
from jsonschema import validate, ValidationError

from .api import calculate, get_schema, submit_to_db, get_history


calculator = Blueprint('calculator', __name__)


@calculator.route('/')
def index():
    return (
        'Welcome to the calculator API! You can post calculation requests '
        'using the following pattern: '
        '"POST /calc {"expression": "-1 * (2 * 6 / 3)"}"')


@calculator.route("/calc", methods=['POST'])
def calc():
    # Validate data
    try:
        data = json.loads(request.data)
        validate(instance=data, schema=get_schema())
    except (json.JSONDecodeError, ValidationError):
        abort(400)

    # Calculate result
    try:
        result = calculate(data["expression"])
    except ValueError:
        abort(400)

    # Store result in database
    db = current_app.config['HYSTORY_DB']
    submit_to_db(db, data["expression"], result['result'])

    return jsonify(result)


@calculator.route("/history", methods=['GET'])
def hist():
    # Get all entries from the database
    db = current_app.config['HYSTORY_DB']
    history = get_history(db)

    return jsonify(history)
