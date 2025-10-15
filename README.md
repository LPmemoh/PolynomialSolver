A Python Polynomial Class (Linked List Implementation)

# Purpose:

This program implements a Polynomial class using a linked list of terms.
It supports the basic algebraic operations on polynomials:

Addition
Subtraction
Multiplication
Division (with quotient and remainder via divmod, or exact division via /)

Polynomials are kept in descending degree order, with no duplicate terms and no zero coefficients stored.
This ensures operations are efficient and results are always simplified.


# Features:

Create polynomials from tuples of (coefficient, degree)
String formatting that produces readable math expressions
Supports integer and fractional coefficients (fractions come from division)

Operators:

\+ : Addition

\- : Subtraction

\* : Multiplication

/ : Exact division (raises error if remainder is non-zero)

divmod(p, q) : Polynomial long division (returns (quotient, remainder))


# Usage Examples:

- Import and construct polynomials:
  ```python
  from PolynomialSolver import Polynomial

  p = Polynomial.from_tuples([(3, 3), (-2, 2), (1, 0)])
  q = Polynomial.from_tuples([(1, 1), (-1, 0)])

  print("p(x) =", p)
  print("q(x) =", q)
  ```

- Basic operations:
  ```python
  print("p + q =", p + q)
  print("p - q =", p - q)
  print("p * q =", p * q)
  ```

- Division:
  ```python
  # Polynomial long division
  quot, rem = divmod(p, q)
  print("quotient:", quot)
  print("remainder:", rem)

  # Exact division (raises if remainder != 0)
  print("p / q =", p / q)
  ```