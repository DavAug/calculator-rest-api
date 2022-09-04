import unittest

from calculator import Expression, calculate


class TestCalculate(unittest.TestCase):
    """Tests the calculate function."""
    def test_call(self):
        # Test call
        result = calculate('123 + 0.05')
        assert result["result"] == '123.05'

        result = calculate('2.2 + 10.31')
        assert result["result"] == '12.51'

        # Test invalid expression
        with self.assertRaisesRegex(ValueError, 'Invalid expression.'):
            calculate('* 123')

        with self.assertRaisesRegex(ValueError, 'Invalid expression.'):
            calculate('{123}')

        with self.assertRaisesRegex(ValueError, 'Invalid expression.'):
            calculate('3 % 2')

        with self.assertRaisesRegex(ValueError, 'Invalid expression.'):
            calculate('3 ] 2')

        with self.assertRaisesRegex(ValueError, 'Invalid expression.'):
            calculate('3 ^ 2')


class TestExpression(unittest.TestCase):
    """Tests the Expression class."""

    def test_addition(self):
        # Case 1
        number = Expression('2 + 3').evaluate()
        self.assertEqual(number, 5)

        # Case 2
        number = Expression('2.2 + 10.31').evaluate()
        self.assertAlmostEqual(number, 12.51)

    def test_division(self):
        # Case 1
        number = Expression('2 / 4').evaluate()
        self.assertEqual(number, 0.5)

        # Case 2
        number = Expression('6 / 10').evaluate()
        self.assertEqual(number, 0.6)

    def test_multiplication(self):
        # Case 1
        number = Expression('2 * 4').evaluate()
        self.assertEqual(number, 8)

        # Case 2
        number = Expression('0.5 * 8').evaluate()
        self.assertEqual(number, 4)

    def test_subtraction(self):
        # Case 1
        number = Expression('12 - 4').evaluate()
        self.assertEqual(number, 8)

        # Case 2
        number = Expression('2 - 4').evaluate()
        self.assertEqual(number, -2)

    def test_leading_operators(self):
        # Case 1
        number = Expression('-4').evaluate()
        self.assertEqual(number, -4)

        # Case 2
        number = Expression('+4').evaluate()
        self.assertEqual(number, 4)

    def test_parentheses(self):
        # Case 1
        number = Expression('(-4 + 10) * 2').evaluate()
        self.assertEqual(number, 12)

        # Case 2
        number = Expression('(1 + 4) * (1 - 6)').evaluate()
        self.assertEqual(number, -25)

        # Case 3
        number = Expression('(((1 + 4) * (1 - 6)))').evaluate()
        self.assertEqual(number, -25)


if __name__ == '__main__':
    unittest.main()
