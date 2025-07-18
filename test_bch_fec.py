import galois
import numpy as np
from bch_fec import P, M, PRIM_POLY
from bch_fec import N, K, S, gf_add, gf_sub, gf_mul, gf_inv, gf_div, gf_log, gf_exp
from bch_fec import bch_enc, bch_dec

rng = np.random.default_rng(12345)

gfe = galois.GF(P, M, irreducible_poly=PRIM_POLY)
bch = galois.BCH(N, K)


def test_gf_add():
    for _ in range(1000):
        a = rng.integers(0, P**M, dtype=int)
        b = rng.integers(0, P**M, dtype=int)

        ref = gf_add(a, b)
        res = gfe(a) + gfe(b)
        assert res == ref


def test_gf_sub():
    for _ in range(1000):
        a = rng.integers(0, P**M, dtype=int)
        b = rng.integers(0, P**M, dtype=int)

        ref = gf_sub(a, b)
        res = gfe(a) - gfe(b)
        assert res == ref


def test_gf_mul():
    for _ in range(1000):
        a = rng.integers(0, P**M, dtype=int)
        b = rng.integers(0, P**M, dtype=int)

        ref = gf_mul(a, b)
        res = gfe(a) * gfe(b)
        assert res == ref


def test_gf_inv():
    for _ in range(1000):
        # Avoid zero to prevent division by zero
        a = rng.integers(1, P**M, dtype=int)

        ref = gfe(a) ** -1
        res = gf_inv(a)
        assert res == ref


def test_gf_div():
    for _ in range(1000):
        a = rng.integers(0, P**M, dtype=int)
        # Avoid zero to prevent division by zero
        b = rng.integers(1, P**M, dtype=int)

        ref = gfe(a) / gfe(b)
        res = gf_div(a, b)
        assert res == ref


def test_gf_log():
    for i in range(1, P**M):
        ref = gfe(i).log()
        res = gf_log(i)
        assert res == ref


def test_gf_exp():
    for i in range(0, P**M - 1):
        ref = gfe(2) ** i
        res = gf_exp(i)
        assert res == ref


def test_bch_enc():
    for _ in range(1000):
        data = rng.integers(0, 2, size=(K - S,), dtype=int)
        parity = bch_enc(data)

        ref = bch.encode(data)
        ref = ref[K - N :]
        assert np.array_equal(parity, ref)


def test_bch_dec():
    for _ in range(1000):
        data = rng.integers(0, 2, size=(K - S,), dtype=int)
        codeword = np.array(bch.encode(data), dtype=int)

        # Introduce error
        error = np.zeros(N - S, dtype=int)
        pos = rng.choice(range(N - S), size=2, replace=False)
        error[N - S - 1 - pos] = 1
        print(pos)

        # Receive codeword with error
        code = np.bitwise_xor(codeword, error)

        # Decode the code
        _, _, decoded = bch_dec(code)

        assert np.array_equal(decoded, codeword), (
            f"Codeword: \n{codeword}\nError: \n{error}\nDecoded: \n{decoded}\n"
        )
