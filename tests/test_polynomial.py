import unittest
from fractions import Fraction

from PolynomialSolver import Polynomial


def poly_to_tuples(poly):
    terms = []
    node = poly._head
    while node is not None:
        terms.append((node.coeff, node.degree))
        node = node.next
    return terms


class PolynomialOperationsTest(unittest.TestCase):
    def test_addition_merges_like_terms(self):
        p = Polynomial([(3, 2), (2, 1), (1, 0)])
        q = Polynomial([(1, 2), (-1, 1)])

        result = p + q

        self.assertEqual(poly_to_tuples(result), [(4, 2), (1, 1), (1, 0)])

    def test_subtraction_handles_negatives(self):
        p = Polynomial([(3, 3), (-2, 2), (1, 0)])
        q = Polynomial([(1, 1), (-1, 0)])

        result = p - q

        self.assertEqual(poly_to_tuples(result), [(3, 3), (-2, 2), (-1, 1), (2, 0)])

    def test_multiplication_combines_degrees(self):
        p = Polynomial([(2, 1), (1, 0)])
        q = Polynomial([(1, 1), (-3, 0)])

        result = p * q

        self.assertEqual(poly_to_tuples(result), [(2, 2), (-5, 1), (-3, 0)])

    def test_divmod_produces_fraction_coefficients(self):
        dividend = Polynomial([(1, 3), (-3, 2), (3, 1), (-1, 0)])
        divisor = Polynomial([(1, 1), (-1, 0)])

        quotient, remainder = divmod(dividend, divisor)

        self.assertEqual(
            poly_to_tuples(quotient),
            [(Fraction(1, 1), 2), (-Fraction(2, 1), 1), (Fraction(1, 1), 0)],
        )
        self.assertTrue(remainder.is_zero())

    def test_truediv_raises_on_non_exact_division(self):
        numerator = Polynomial([(1, 2), (1, 0)])
        denominator = Polynomial([(1, 1), (1, 0)])

        with self.assertRaises(ValueError):
            _ = numerator / denominator


if __name__ == "__main__":
    unittest.main()
