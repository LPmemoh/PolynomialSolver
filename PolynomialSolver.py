# -------------------------
# Author: Liam Prsa
# Purpose: This program allows for polynomials to be added, subtracted, multiplied, and divided
# -------------------------

from fractions import Fraction

class Polynomial:
    """
    Polynomial implemented as a singly-linked list of terms.
    Invariant:
      - Terms are kept sorted by degree (DESCENDING).
      - No zero-coefficient terms are stored.
      - No duplicate degrees.
    """

    class Term:
        def __init__(self, coefficient: int, degree: int, next_node=None):
            self.coeff = coefficient
            self.degree = degree
            self.next = next_node

        def __str__(self):
            return f"{self.coeff} {self.degree}"

    def __init__(self, tuples=None):
        """
        Build from an optional tuple of (coeff, degree) tuples.
        """
        self._head = None
        self._size = 0
        if tuples:
            for c, d in tuples:
                self._insert_term_invariant(c, d)

    # ---------- basic helpers ----------

    def is_empty(self) -> bool:
        return self._head is None

    def is_zero(self) -> bool:
        """Zero polynomial iff there are no terms."""
        return self._head is None

    def degree(self) -> int:
        """Return highest degree, or 0 for an empty polynomial"""
        if self._head is None:
            return 0
        return self._head.degree  # list kept in descending order

    # ---------- core invariant insert ----------

    def _insert_term_invariant(self, coeff: int, degree: int):
        """
        Insert (coeff, degree) while preserving invariants:
          - descending degree order
          - merge same degree
          - drop zero coefficients
        """
        if coeff == 0:
            return

        # If empty or new degree is larger than current head degree -> insert at head
        if self._head is None or degree > self._head.degree:
            self._head = self.Term(coeff, degree, self._head)
            self._size += 1
            return

        # Walk until the correct spot (descending degrees)
        prev = None
        cur = self._head
        while cur and cur.degree > degree:
            prev = cur
            cur = cur.next

        if cur and cur.degree == degree:
            # Merge coefficients
            cur.coeff += coeff
            # Drop if it becomes zero
            if cur.coeff == 0:
                if prev is None:  # removing head
                    self._head = cur.next
                else:
                    prev.next = cur.next
                self._size -= 1
            return

        # Insert before 'cur' (which has smaller degree) or at end
        new_node = self.Term(coeff, degree, cur)
        if prev is None:
            self._head = new_node
        else:
            prev.next = new_node
        self._size += 1

    # ---------- string representation ----------

    def __str__(self) -> str:
        if self._head is None:
            return "0"

        parts = []
        node = self._head
        while node:
            c, d = node.coeff, node.degree

            # sign & magnitude
            sign = "+" if c > 0 else "-"
            mag = abs(c)

            if d == 0:
                term = f"{mag}"
            elif d == 1:
                if mag == 1:
                    term = "x"
                else:
                    term = f"{mag}x"
            else:
                if mag == 1:
                    term = f"x^{d}"
                else:
                    term = f"{mag}x^{d}"

            parts.append((sign, term))
            node = node.next

        # Build with proper leading sign
        first_sign, first_term = parts[0]
        s = ""
        s += first_term if first_sign == "+" else f"- {first_term}"

        for sign, term in parts[1:]:
            s += f" {sign} {term}"

        return s

    # ---------- operator overloads ----------

    def __add__(self, other):
        if not isinstance(other, Polynomial):
            raise TypeError("Can only add Polynomial to Polynomial.")

        res = Polynomial()
        a, b = self._head, other._head

        while a is not None and b is not None:
            if a.degree > b.degree:
                res._insert_term_invariant(a.coeff, a.degree)
                a = a.next
            elif a.degree < b.degree:
                res._insert_term_invariant(b.coeff, b.degree)
                b = b.next
            else:
                s = a.coeff + b.coeff
                if s != 0:
                    res._insert_term_invariant(s, a.degree)
                a, b = a.next, b.next

        while a is not None:
            res._insert_term_invariant(a.coeff, a.degree)
            a = a.next

        while b is not None:
            res._insert_term_invariant(b.coeff, b.degree)
            b = b.next

        return res

    def __mul__(self, other):
        if not isinstance(other, Polynomial):
            raise TypeError("Can only multiply Polynomial by Polynomial.")

        # Accumulate products directly into result; insert merges degrees/drops zeros
        res = Polynomial()
        a = self._head
        while a is not None:
            b = other._head
            while b is not None:
                res._insert_term_invariant(a.coeff * b.coeff, a.degree + b.degree)
                b = b.next
            a = a.next
        return res

    # ---------- sign & subtraction ----------

    def __neg__(self):
        """Unary minus: return -self."""
        res = Polynomial()
        node = self._head
        while node:
            res._insert_term_invariant(-node.coeff, node.degree)
            node = node.next
        return res

    def __sub__(self, other):
        """p - q == p + (-q)"""
        if not isinstance(other, Polynomial):
            raise TypeError("Can only subtract Polynomial from Polynomial.")
        return self + (-other)

    # ---------- division helpers ----------

    def _leading_term(self):
        """
        Return (coeff, degree) of the leading term, or (0, 0) if zero polynomial.
        Coeff is returned as an int for internal use.
        """
        if self._head is None:
            return 0, 0
        return self._head.coeff, self._head.degree

    def _mul_monomial(self, coeff, degree):
        """
        Return self * (coeff*x^degree). coeff can be int or Fraction.
        """
        res = Polynomial()
        node = self._head
        while node:
            # Allow Fraction coefficients during division
            new_c = (Fraction(node.coeff) if not isinstance(node.coeff, Fraction) else node.coeff) * Fraction(coeff)
            res._insert_term_invariant(new_c, node.degree + degree)
            node = node.next
        return res

    def _as_fraction_poly(self):
        """
        Convert all coefficients to Fractions (used by division to stay exact).
        """
        res = Polynomial()
        node = self._head
        while node:
            res._insert_term_invariant(Fraction(node.coeff), node.degree)
            node = node.next
        return res

    # ---------- division (long division) ----------

    def __divmod__(self, other):
        """
        Polynomial long division: returns (quotient, remainder) so that
        self = other*quotient + remainder, and degree(remainder) < degree(other) or remainder == 0.

        Coefficients in quotient/remainder are Fractions for exactness.
        """
        if not isinstance(other, Polynomial):
            raise TypeError("Can only divide Polynomial by Polynomial.")
        if other.is_zero():
            raise ZeroDivisionError("Polynomial division by zero polynomial.")

        # Work in Fractions to keep exact arithmetic.
        dividend = self._as_fraction_poly()
        divisor = other._as_fraction_poly()

        q = Polynomial()  # quotient (Fractions)
        r = Polynomial()  # running remainder (Fractions)
        # Start with r = dividend
        node = dividend._head
        while node:
            r._insert_term_invariant(node.coeff, node.degree)
            node = node.next

        # Long division
        d_lead_c, d_lead_deg = divisor._leading_term()
        while (not r.is_zero()) and (r.degree() >= d_lead_deg):
            r_lead_c, r_lead_deg = r._leading_term()
            # term_to_cancel = (r_lead_c / d_lead_c) * x^(r_lead_deg - d_lead_deg)
            factor_c = Fraction(r_lead_c) / Fraction(d_lead_c)
            factor_deg = r_lead_deg - d_lead_deg

            # q += factor
            q._insert_term_invariant(factor_c, factor_deg)
            # r -= divisor * factor
            r = r - divisor._mul_monomial(factor_c, factor_deg)

        # Ensure quotient/remainder keep invariants and Fractions are preserved
        return q, r

    def __truediv__(self, other):
        """
        Exact division: returns quotient if remainder is zero, else raises.
        """
        q, r = divmod(self, other)
        if r.is_zero():
            return q
        raise ValueError(
            "Polynomial division not exact (non-zero remainder). Use divmod(p, q) for quotient and remainder.")

    # ---------- testing ----------

    '''
    Ex. Usage: p = Polynomial.from_tuples([(3,3), (-2,2), (1,0)])   # 3x^3 - 2x^2 + 1
    q = Polynomial.from_tuples([(1,1), (-1,0)])          # x - 1

    -- Subtraction --
    print(p - q)          # 3x^3 - 2x^2 - x + 2

    -- Division (long division) --
    quot, rem = divmod(p, q)
    print("q:", quot)     # expected: 3x^2 + x - 1  (with Fraction coeffs if needed)
    print("r:", rem)      # expected: 0

    -- Exact division --
    print(p / q)          # 3x^2 + x - 1
    '''

    @classmethod
    def from_tuples(cls, tuples):
        """Build polynomial from tuple of (coeff, degree)."""
        return cls(tuples)