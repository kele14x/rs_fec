import galois
import numpy as np
import matplotlib.pyplot as plt


if __name__ == "__main__":
    # Define the BCH code parameters
    p = 2
    m = 1
    n = 1023
    k = 1003
    t = 2
    s = 491

    gf = galois.GF(p**m)
    bch = galois.BCH(n, k, field=gf)

    l = 10000
    nus = np.arange(24)  # Number of errors to test
    p = np.zeros(len(nus))
    for i, nu in enumerate(nus):
        decode_mismatch = 0
        for _ in range(l):
            # Generate a random message
            message = gf(np.random.randint(2, size=k - s, dtype=int))
            # Encode the message
            codeword = bch.encode(message)
            # Introduce errors
            error_positions = np.random.choice(n - s, size=nu, replace=False)
            errors = gf(np.zeros(n - s, dtype=int))
            errors[error_positions] = gf(1)
            # Add errors to the codeword
            received = codeword + errors
            # Decode the received codeword
            decoded, n_error = bch.decode(received, output="codeword", errors=True)
            # Check if the decoder reported number of errors
            if n_error >= 0 and not np.array_equal(decoded, codeword):
                # it rarely decoded codeword matches the original codeword so skip check?
                decode_mismatch += 1

        print(f"Testing with nu = {nu}")
        print(f"Number of decode mismatches: {decode_mismatch} out of {l} trials")
        print(f"Mismatch rate: {decode_mismatch / l:.4f}")
        p[i] = decode_mismatch / l

    plt.figure()
    plt.plot(nus, p * 100, marker="o")
    plt.xlabel("Number of errors (nu)")
    plt.ylabel("Mismatch rate (p / %)")
    plt.title("BCH (532, 512)\nMismatch Rate vs Number of Errors")
    plt.grid(True)
    plt.show()
