#!/usr/bin/env python3

import galois
import numpy as np

# The definition of GF(2^8)
P = 2
M = 8
PRIM_POLY = 285  # x^8 + x^4 + x^3 + x^2 + 1
PRIM_ELEMENT = 2

# The definition of RS(68, 64)
N = 2**M - 1
T = 2
K = N - T * 2
S = 187
c = 0


if __name__ == "__main__":
    rs = galois.ReedSolomon(N, K, c=c)
    GF = rs.field

    code = np.genfromtxt("code.csv", dtype=int, delimiter=",")
    cnumerr = np.genfromtxt("cnumerr.csv", dtype=int, delimiter=",")
    ccode = np.genfromtxt("ccode.csv", dtype=int, delimiter=",")

    ccode2, cnumerr2 = rs.decode(code, output="codeword", errors=True)

    assert np.array_equal(ccode, ccode2)
    assert np.array_equal(cnumerr, cnumerr2)
    print("All tests passed!")
