from rs_fec import P, M, GF, gf_add, gf_sub, gf_mul, gf_inv, gf_div
import numpy as np


def test_gf_addition():
    """Test the Galois Field addition."""
    for _ in range(1000):
        a = np.random.randint(0, P**M)
        b = np.random.randint(0, P**M)
        expected = GF(a) + GF(b)
        result = gf_add(a, b)
        assert result == expected, f"Expected {expected}, got {result}"


def test_gf_subtraction():
    """Test the Galois Field subtraction."""
    for _ in range(1000):
        a = np.random.randint(0, P**M)
        b = np.random.randint(0, P**M)
        expected = GF(a) - GF(b)
        result = gf_sub(a, b)
        assert result == expected, f"Expected {expected}, got {result}"


def test_gf_multiplication():
    """Test the Galois Field multiplication."""
    for _ in range(1000):
        a = np.random.randint(0, P**M)
        b = np.random.randint(0, P**M)
        expected = GF(a) * GF(b)
        result = gf_mul(a, b)
        assert result == expected, f"Expected {expected}, got {result}"


def test_gf_inverse():
    """Test the Galois Field inverse."""
    for _ in range(1000):
        a = np.random.randint(1, P**M)  # Avoid zero to prevent division by zero
        expected = GF(a) ** -1
        result = gf_inv(a)
        assert result == expected, f"Expected {expected}, got {result}"


def test_gf_division():
    """Test the Galois Field division."""
    for _ in range(1000):
        a = np.random.randint(0, P**M)
        b = np.random.randint(1, P**M)  # Avoid zero to prevent division by zero
        expected = GF(a) / GF(b)
        result = gf_div(a, b)  # Division is multiplication by the inverse
        assert result == expected, f"Expected {expected}, got {result}"
