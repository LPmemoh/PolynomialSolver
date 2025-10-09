A Python Polynomial Class (Linked List Implementation)

# Purpose:

This program implements a Polynomial class using a linked list of terms.
It supports the basic algebraic operations on polynomials:

Addition
Subtraction
Multiplication
Division (with quotient & remainder via divmod, or exact division via /)

Polynomials are kept in descending degree order, with no duplicate terms and no zero coefficients stored.
This ensures operations are efficient and results are always simplified.


# Features:

Create polynomials from tuples of (coefficient, degree)
Convert polynomials back to tuple lists for testing or serialization
String formatting that produces readable math expressions
Supports integer and fractional coefficients (fractions come from division)

Operators:

+ : Addition

- : Subtraction

* : Multiplication

/ : Exact division (raises error if remainder is non-zero)

divmod(p, q) : Polynomial long division (returns (quotient, remainder))


# Usage Examples:

from polynomial import Polynomial

Create polynomials
p = Polynomial.from_tuples([(3, 3), (-2, 2), (1, 0)])   # 3x^3 - 2x^2 + 1
q = Polynomial.from_tuples([(1,1), (-1,0)])       # x - 1

print("p(x) =", p)   # p(x) = 3x^3 - 2x^2 + 1
print("q(x) =", q)   # q(x) = x - 1

Addition
print("p + q =", p + q)   # 3x^3 - 2x^2 + x

Subtraction
print("p - q =", p - q)   # 3x^3 - 2x^2 - x + 2

Multiplication
print("p * q =", p * q)   # 3x^4 - 5x^3 + 2x^2 + x - 1

Division (long division)
quot, rem = divmod(p, q)
print("quotient:", quot)  # 3x^2 + x - 1
print("remainder:", rem)  # 0

Exact division
print("p / q =", p / q)   # 3x^2 + x - 1
