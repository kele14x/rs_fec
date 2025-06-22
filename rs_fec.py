import numpy as np
import galois

# The definition of GF(2^8)
P = 2
M = 8
PRIM_POLY = 285  # x^8 + x^4 + x^3 + x^2 + 1
PRIM_ELEMENT = 2
GF = galois.GF(P**M, irreducible_poly=PRIM_POLY, primitive_element=PRIM_ELEMENT)

# RS(68, 64), RS(N - S, K - S)
N = 2**M - 1
T = 2
K = N - T * 2
S = 187

# The log and the exponent table for quick calculation

# The log table calculates the q = log_alpha(a) for none-zero elements a in GF(2^8)
# Note: The log table is indexed by the value of a, which is in the range [1, P**M - 1]
#       The LOG_TABLE[0] is invalid and should not be used.
#       The output range is [0, P**M - 2]
LOG_TABLE = np.zeros(P**M, dtype=int)
for i in range(P**M - 1):
    a = GF(2) ** i
    LOG_TABLE[a] = i

# The exponent table calculates the q = alpha^a for a in [0, P**M - 2]
# Note: The input range is [0, P**M - 2] and the output range is [1, P**M - 1]
EXP_TABLE = np.zeros(P**M, dtype=int)
for i in range(P**M):
    EXP_TABLE[i] = GF(2) ** i


def gf_add(a: int, b: int):
    """GF(2^8) addition"""
    if a != a & 0xFF:
        raise ValueError("a is not a valid GF(2^8) element")
    if b != b & 0xFF:
        raise ValueError("b is not a valid GF(2^8) element")
    return a ^ b


def gf_sub(a: int, b: int):
    """GF(2^8) subtraction"""
    # Subtraction is the same as addition in GF(2^8)
    return gf_add(a, b)


def gf_mul(a: int, b: int):
    if a != a & 0xFF:
        raise ValueError("a is not a valid GF(2^8) element")
    if b != b & 0xFF:
        raise ValueError("b is not a valid GF(2^8) element")

    if a == 0 or b == 0:
        return 0
    log_a = LOG_TABLE[a]
    log_b = LOG_TABLE[b]
    log_result = (log_a + log_b) % (P**M - 1)
    return EXP_TABLE[log_result]


def gf_inv(a: int):
    if a != a & 0xFF:
        raise ValueError("a is not a valid GF(2^8) element")
    if a == 0:
        raise ZeroDivisionError("Inverse of zero is undefined in GF(2^8)")

    log_a = LOG_TABLE[a]
    log_result = (-log_a) % (P**M - 1)
    return EXP_TABLE[log_result]


def gf_div(a: int, b: int):
    if a != a & 0xFF:
        raise ValueError("a is not a valid GF(2^8) element")
    if b != b & 0xFF:
        raise ValueError("b is not a valid GF(2^8) element")

    if b == 0:
        raise ZeroDivisionError("Division by zero is undefined in GF(2^8)")
    if a == 0:
        return 0
    log_a = LOG_TABLE[a]
    log_b = LOG_TABLE[b]
    # Ensure the result is in the range [0 to P**M - 2]
    log_result = (log_a - log_b) % (P**M - 1)
    return EXP_TABLE[log_result]


if __name__ == "__main__":
    print("Log table of GF(2^8): ")
    print(LOG_TABLE)
    print("\nExp table of GF(2^8): ")
    print(EXP_TABLE)
