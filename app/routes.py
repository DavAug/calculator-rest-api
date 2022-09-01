from flask import Blueprint, request, abort


calculator = Blueprint('calculator', __name__)


@calculator.route('/')
def index():
    return (
        'Welcome to the calculator API! You can post calculation requests '
        'using the following pattern: '
        '"POST /calc {"expression": "-1 * (2 * 6 / 3)"} "')


@calculator.route("/calc", methods=['POST'])
def calc():
    if request.json:
        return request.json
    else:
        abort(404)
