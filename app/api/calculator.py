
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
    # Parse expression
    number = Number(expression)
    try:
        number = number.evaluate()
    except ValueError:
        raise ValueError("Invalid expression. Expression cannot be evaluated.")

    # For cosmetics, convert float into integer when number is an integer
    number = int(number) if number.is_integer() else number

    return {"result": str(number)}


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


class Number():
    """
    Defines a number based on the evaluation of a string expression.

    :param expression: Expression.
    :type expression: str
    """
    def __init__(self, expression):
        # Remove spaces from expression
        self._expression = str(expression).replace(" ", "")

        # Check whether expression is ready to be converted to float
        # (i.e. expression does not contain operations)
        self._is_ready = not (
            ('+' in self._expression) |
            ('-' in self._expression) |
            ('*' in self._expression) |
            ('/' in self._expression) |
            ('(' in self._expression) |
            (')' in self._expression)
        )

    def _eval_addition(self, expression):
        """
        Splits the expression based on the addition operator and
        returns a new expression with the evaluated addition result.

        :param expression: Expression.
        :type expression: str

        :rtype: str
        """
        operator_index = expression.find('+')

        # Return expression if it doesn't contain any additions
        if (operator_index == -1) or (operator_index == 0):
            return expression

        # Evaluate expression
        left = Number(expression[:operator_index]).evaluate()
        right = Number(expression[operator_index+1:]).evaluate()
        expression = f'{left + right:.14f}'

        return expression

    def _eval_division(self, expression):
        """
        Splits the expression based on the division operator and
        returns a new expression with the evaluated division result.

        :param expression: Expression.
        :type expression: str

        :rtype: str
        """
        operator_index = expression.find('/')

        # Return expression if it doesn't contain any division
        if operator_index == -1:
            return expression

        # Evaluate expression
        left = Number(expression[:operator_index]).evaluate()
        right = Number(expression[operator_index+1:]).evaluate()
        expression = f'{left / right:.14f}'

        return expression

    def _eval_multiplication(self, expression):
        """
        Splits the expression based on the multiplication operator and
        returns a new expression with the evaluated multiplication result.

        :param expression: Expression.
        :type expression: str

        :rtype: str
        """
        operator_index = expression.find('*')

        # Return expression if it doesn't contain any multiplication
        if operator_index == -1:
            return expression

        # Evaluate expression
        left = Number(expression[:operator_index]).evaluate()
        right = Number(expression[operator_index+1:]).evaluate()
        expression = f'{left * right:.14f}'

        return expression

    def _eval_parentheses(self, expression):
        """
        Splits the expression based on the parentheses and returns a new
        expression, where the expression in the paranthesis is evaluated.

        :param expression: Expression.
        :type expression: str

        :rtype: str
        """
        # Find bracket in expression
        start = expression.find('(')
        end = start + expression[start:].find(')')

        # Check that there are no interior opening brackets
        index = 0
        while index != -1:
            start += index
            index = expression[start+1:end].find('(')
        start += index + 1

        # Insert evalutated paranthesis into expression
        inside = expression[start+1:end]
        number = Number(inside).evaluate()
        expression = \
            expression[:start] + str(number) + expression[end+1:]

        return expression

    def _eval_subtraction(self, expression):
        """
        Splits the expression based on the subtraction operator and
        returns a new expression with the evaluated subtraction result.

        :param expression: Expression.
        :type expression: str

        :rtype: str
        """
        operator_index = expression.find('-')

        # Return expression if it doesn't contain any subtractions
        if (operator_index == -1) or (operator_index == 0):
            return expression

        # Evaluate expression
        left = Number(expression[:operator_index]).evaluate()
        right = Number(expression[operator_index+1:]).evaluate()
        expression = f'{left - right:.14f}'

        return expression

    def evaluate(self):
        """
        Returns the evaluated expression as a float.

        :rtype: float
        """
        # Try easy case: expression does not contain operators or parantheses.
        if self._is_ready:
            number = float(self._expression)
            return number

        # Parse expression based on parentheses
        expression = self._expression
        if '(' in expression:
            expression = self._eval_parentheses(expression)

        # Parse expression based on operators
        if '*' in expression:
            expression = self._eval_multiplication(expression)
        if '/' in expression:
            expression = self._eval_division(expression)
        if '+' in expression:
            expression = self._eval_addition(expression)
        if '-' in expression:
            expression = self._eval_subtraction(expression)

        # Convert expression to float
        number = float(expression)

        return number
