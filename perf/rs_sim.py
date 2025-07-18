import galois
import numpy as np
import matplotlib.pyplot as plt


def rs_mismatch_vs_nu(l=10000):
    # Define the Reed-Solomon code parameters
    p = 2
    m = 8
    n = 255
    k = 251
    prim_poly = 0x11D
    s = 187

    gf = galois.GF(p**m, irreducible_poly=prim_poly)
    rs = galois.ReedSolomon(n, k, field=gf)

    p = np.zeros(10)
    for nu in range(10):
        decode_mismatch = 0
        for _ in range(l):
            # Generate a random message
            message = gf(np.random.randint(0, n + 1, size=k - s, dtype=int))
            # Encode the message
            codeword = rs.encode(message)
            # Introduce errors
            error_positions = np.random.choice(n - s, size=nu, replace=False)
            error_values = gf(np.random.choice(np.arange(1, n + 1), size=nu))
            errors = gf(np.zeros(n - s, dtype=int))
            errors[error_positions] = error_values
            # Add errors to the codeword
            received = codeword + errors
            # Decode the received codeword
            decoded, n_error = rs.decode(received, output="codeword", errors=True)
            # Check if the decoder reported number of errors
            if n_error >= 0 and not np.array_equal(decoded, codeword):
                # it rarely decoded codeword matches the original codeword so skip check?
                decode_mismatch += 1

        print(f"Testing with nu = {nu}")
        print(f"Number of decode mismatches: {decode_mismatch} out of {l} trials")
        print(f"Mismatch rate: {decode_mismatch / l:.4f}")
        p[nu] = decode_mismatch / l

    plt.figure()
    plt.plot(range(10), p * 100, marker="o")
    plt.xlabel("Number of errors (nu)")
    plt.ylabel("Mismatch rate (p / %)")
    plt.title("RS (68, 64)\nMismatch Rate vs Number of Errors")
    plt.grid(True)
    plt.show()


def rs_ber_vs_p(l: int = 10000):
    # Define the Reed-Solomon code parameters
    p = 2
    m = 8
    n = 255
    k = 251
    prim_poly = 0x11D
    s = 187

    gf = galois.GF(p**m, irreducible_poly=prim_poly)
    rs = galois.ReedSolomon(n, k, field=gf)

    ber = np.zeros(10)
    for nu in range(10):
        bit_errors = 0
        for _ in range(l):
            # Generate a random message
            message = gf(np.random.randint(0, n + 1, size=k - s, dtype=int))
            # Encode the message
            codeword = rs.encode(message)
            # Introduce errors
            error_positions = np.random.choice(n - s, size=nu, replace=False)
            error_values = gf(np.random.choice(np.arange(1, n + 1), size=nu))
            errors = gf(np.zeros(n - s, dtype=int))
            errors[error_positions] = error_values
            # Add errors to the codeword
            received = codeword + errors
            # Decode the received codeword
            decoded, n_error = rs.decode(received, output="codeword", errors=True)
            # Count bit errors if decoding was successful
            if n_error >= 0 and not np.array_equal(decoded, codeword):
                bit_errors += np.sum(decoded != codeword)

        print(f"Testing with nu = {nu}")
        print(f"Number of bit errors: {bit_errors} out of {l * (n - s)} trials")
        ber[nu] = bit_errors / (l * (n - s))

    plt.figure()
    plt.plot(range(10), ber * 100, marker="o")
    plt.xlabel("Number of errors (nu)")
    plt.ylabel("Bit Error Rate (BER / %)")
    plt.title("RS (68, 64)\nBit Error Rate vs Number of Errors")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    rs_mismatch_vs_nu(l=10000)
