import json

from flask import Blueprint, abort, jsonify, request
from jsonschema import validate, ValidationError

from .api import calculator as calculator_api


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
        validate(instance=data, schema=calculator_api.get_schema())
    except (json.JSONDecodeError, ValidationError):
        abort(400)

    # Calculate result
    result = calculator_api.calculate(data["expression"])
    try:
        result = calculator_api.calculate(data["expression"])
    except ValueError:
        abort(400)

    return jsonify(result)
