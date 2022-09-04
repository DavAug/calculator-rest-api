
def calculate(expression):
    """
    Computes the expression and returns a JSON with the result.

    Supported operations are
        1. addition: +
        2. subtraction: -
        3. multiplication: *
        4. division: /

    Each operation is pairwise.

    Supported parenthesis are "(" and ")".

    Spaces are ignored.

    :param expression: Expression
    :type expression: str

    :rtype: dict
    """
    # Evaluate expression
    number = Expression(expression).evaluate()

    # For cosmetics:
    if number.is_integer():
        # convert float into integer when number is an integer
        number = str(int(number))
    else:
        # Round to floating precision and remove trailing decimal zeros
        number = str(round(number, ndigits=14))

    return {"result": number}


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


class Expression():
    """
    Defines an expression from a string.

    Supported operators are +, -, *, /. Supported parenthesis are ( and ).

    :param expression: Expression.
    :type expression: str
    """
    def __init__(self, expression):
        # Remove spaces from expression
        self._expression = str(expression).replace(" ", "")

    def _find_operator_index(self, expression, op):
        """
        Returns the operator index following precedence of parentheses.
        """
        operator_index = expression.find(op)
        start = expression.find('(')

        # If no parentheses exist or operator is before opening parenthesis,
        # return
        if (start == -1) or (operator_index <= start):
            return operator_index

        # Find matching closing parenthesis and return operator to the right
        end = start + expression[start:].find(')')
        another_opening = expression[start+1:end].find('(') + 1
        while another_opening != -1:
            start += another_opening + 1
            end = start + expression[start:].find(')')
            another_opening = expression[start+1:end].find('(')
        operator_index = end + 1

        # If no operator exists to the right, continue to the next operator
        if operator_index >= len(expression):
            return -1

        return operator_index

    def _parse_expression(self):
        """
        Parses the expression.

        The expression is parsed to

            - a float, if the expression contains no operators (except leading
                operators, such as -2, or +10.
            - or an expression-operator-expression triplet if the expression
                contains operators.

        The expression-operator-expression follows operator precedence.

        :rtype: (float, None, None) or (Expression, str, Expression)
        """
        # Remove encapsulating parentheses
        expression = self._remove_parentheses(self._expression)

        # Parse expression into expression-operator-expression triplet
        # following operator precedence.
        for op in ['*', '/', '+', '-']:
            left, right = self._parse_triplet(expression, op)
            if left:
                return Expression(left), op, Expression(right)

        # No operators and parentheses are left. So float can be returned.
        try:
            number = float(expression)
        except ValueError:
            raise ValueError(
                "Invalid expression. Expression cannot be evaluated.")

        return number, None, None

    def _parse_triplet(self, expression, op):
        """
        Splits the expression at the operator location.
        """
        left, right = None, None
        operator_index = self._find_operator_index(expression, op)
        if (operator_index != -1) and (operator_index != 0):
            left = expression[:operator_index]
            right = expression[operator_index+1:]

        return left, right

    def _remove_parentheses(self, expression):
        """
        Strips encapsulating parentheses from the expression.

        Starts from the innermost parentheses and iteratively goes to the
        outmost parentheses. If the outmost parentheses are the first and
        last element in the expression, they are removed.

        Algorithm is applied recursively to ensure that multiple layers of
        encapsuating parentheses are removed.

        :rtype: str
        """
        # Iteratively remove expression inside innermost parentheses, and stop
        # when no parantheses are left, or parentheses are first and last
        # element in expression
        e = expression
        end = 0
        while end != -1:
            # Find innermost bracket
            end = e.find(')')
            start = end - e[:end][::-1].find('(') - 1

            # Check whether parentheses encapsulate whole expression
            if (start == 0) and ((end + 1) == len(e)):
                return self._remove_parentheses(expression[1:-1])

            # Remove inner expression
            e = e[:start] + e[end+1:]

        return expression

    def evaluate(self):
        """
        Returns the evaluated expression.

        :rtype: float
        """
        left, op, right = self._parse_expression()
        if not op:
            # Expression requires no further evaluation
            return left

        # Perform pairwise operation
        # NOTE: left and right expressions are recursively evaluated.
        if op == '*':
            return left.evaluate() * right.evaluate()
        if op == '/':
            return left.evaluate() / right.evaluate()
        if op == '+':
            return left.evaluate() + right.evaluate()

        return left.evaluate() - right.evaluate()
