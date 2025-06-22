from rs_fec import P, M, PRIM_POLY, PRIM_ELEMENT, LOG_TABLE, EXP_TABLE
from rs_fec import N, K, T, S
from rs_fec import gf_add, gf_sub, gf_mul, gf_inv, gf_div
from rs_fec import rs_enc

import numpy as np
import galois

GF = galois.GF(P**M, irreducible_poly=PRIM_POLY, primitive_element=PRIM_ELEMENT)
RS = galois.ReedSolomon(N, K)


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


def test_gf_log_table():
    """Test the Galois Field log table."""
    for i in range(0, P**M - 1):
        expected = i
        result = LOG_TABLE[GF(2) ** i]
        assert expected == result, f"Expected {expected}, got {result}"


def test_gf_exp_table():
    """Test the Galois Field exponentiation table."""
    for i in range(0, P**M - 1):
        expected = GF(2) ** i
        result = EXP_TABLE[i]
        assert expected == result, f"Expected {expected}, got {result}"


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
        result = gf_div(a, b)
        assert result == expected, f"Expected {expected}, got {result}"


def test_rs_encoding():
    """Test the Reed-Solomon encoding."""
    for _ in range(1000):
        msg = np.random.randint(0, P**M, size=K - S, dtype=np.int64)
        expected = RS.encode(msg)
        expected = expected[-T * 2 :]  # Get the last T * 2 elements as parity
        result = rs_enc(msg)

        assert np.array_equal(result, expected), f"Expected {expected}, got {result}"
