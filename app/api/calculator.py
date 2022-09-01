def calculate(data):
    # Parse data

    return {"result": "Test result"}


def get_schema():
    """
    Returns a schema for the input data to the calculator.

    :rtype: dict
    """
    schema = {
        "type": "object",
        "required": ["expression"],
        "properties": {
            "expression": {"type": "string"},
        },
    }

    return schema
