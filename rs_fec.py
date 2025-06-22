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

# The log and the exponent table for quick calculation

# The log table calculates the q = log_alpha(a) for none-zero elements a in GF(2^8)
# Note: The log table is indexed by the value of a, which is in the range [1, P**M - 1]
#       The LOG_TABLE[0] is invalid and should not be used.
#       The output range is [0, P**M - 2]
# fmt: off
LOG_TABLE = np.array([
     -1,   0,   1,  25,   2,  50,  26, 198,   3, 223,  51, 238,  27, 104, 199,  75,
      4, 100, 224,  14,  52, 141, 239, 129,  28, 193, 105, 248, 200,   8,  76, 113,
      5, 138, 101,  47, 225,  36,  15,  33,  53, 147, 142, 218, 240,  18, 130,  69,
     29, 181, 194, 125, 106,  39, 249, 185, 201, 154,   9, 120,  77, 228, 114, 166,
      6, 191, 139,  98, 102, 221,  48, 253, 226, 152,  37, 179,  16, 145,  34, 136,
     54, 208, 148, 206, 143, 150, 219, 189, 241, 210,  19,  92, 131,  56,  70,  64,
     30,  66, 182, 163, 195,  72, 126, 110, 107,  58,  40,  84, 250, 133, 186,  61,
    202,  94, 155, 159,  10,  21, 121,  43,  78, 212, 229, 172, 115, 243, 167,  87,
      7, 112, 192, 247, 140, 128,  99,  13, 103,  74, 222, 237,  49, 197, 254,  24,
    227, 165, 153, 119,  38, 184, 180, 124,  17,  68, 146, 217,  35,  32, 137,  46,
     55,  63, 209,  91, 149, 188, 207, 205, 144, 135, 151, 178, 220, 252, 190,  97,
    242,  86, 211, 171,  20,  42,  93, 158, 132,  60,  57,  83,  71, 109,  65, 162,
     31,  45,  67, 216, 183, 123, 164, 118, 196,  23,  73, 236, 127,  12, 111, 246,
    108, 161,  59,  82,  41, 157,  85, 170, 251,  96, 134, 177, 187, 204,  62,  90,
    203,  89,  95, 176, 156, 169, 160,  81,  11, 245,  22, 235, 122, 117,  44, 215,
     79, 174, 213, 233, 230, 231, 173, 232, 116, 214, 244, 234, 168,  80,  88, 175,
], dtype=int)
# fmt: on

# The exponent table calculates the q = alpha^a for a in [0, P**M - 2]
# Note: The input range is [0, P**M - 2] and the output range is [1, P**M - 1]
# fmt: off
EXP_TABLE = np.array([
      1,   2,   4,   8,  16,  32,  64, 128,  29,  58, 116, 232, 205, 135,  19,  38,
     76, 152,  45,  90, 180, 117, 234, 201, 143,   3,   6,  12,  24,  48,  96, 192,
    157,  39,  78, 156,  37,  74, 148,  53, 106, 212, 181, 119, 238, 193, 159,  35,
     70, 140,   5,  10,  20,  40,  80, 160,  93, 186, 105, 210, 185, 111, 222, 161,
     95, 190,  97, 194, 153,  47,  94, 188, 101, 202, 137,  15,  30,  60, 120, 240,
    253, 231, 211, 187, 107, 214, 177, 127, 254, 225, 223, 163,  91, 182, 113, 226,
    217, 175,  67, 134,  17,  34,  68, 136,  13,  26,  52, 104, 208, 189, 103, 206,
    129,  31,  62, 124, 248, 237, 199, 147,  59, 118, 236, 197, 151,  51, 102, 204,
    133,  23,  46,  92, 184, 109, 218, 169,  79, 158,  33,  66, 132,  21,  42,  84,
    168,  77, 154,  41,  82, 164,  85, 170,  73, 146,  57, 114, 228, 213, 183, 115,
    230, 209, 191,  99, 198, 145,  63, 126, 252, 229, 215, 179, 123, 246, 241, 255,
    227, 219, 171,  75, 150,  49,  98, 196, 149,  55, 110, 220, 165,  87, 174,  65,
    130,  25,  50, 100, 200, 141,   7,  14,  28,  56, 112, 224, 221, 167,  83, 166,
     81, 162,  89, 178, 121, 242, 249, 239, 195, 155,  43,  86, 172,  69, 138,   9,
     18,  36,  72, 144,  61, 122, 244, 245, 247, 243, 251, 235, 203, 139,  11,  22,
     44,  88, 176, 125, 250, 233, 207, 131,  27,  54, 108, 216, 173,  71, 142,  -1,
], dtype=int)
# fmt: on

# The generator matrix G for RS(68, 64)
# fmt: off
G = np.array([
    [241,  12, 191,  74],
    [ 12, 121, 197, 111],
    [ 10, 192,  90, 125],
    [243,  90, 186, 136],
    [182,  22, 187,  75],
    [229,  95, 135, 215],
    [230,  46, 187, 223],
    [253,   2,  48, 106],
    [ 96, 201,   4, 254],
    [120,  89,  64, 119],
    [ 39, 197, 105, 126],
    [213, 212,  87,  98],
    [123, 206,  40,  16],
    [ 54,  37,  39,  39],
    [201, 176, 127,  42],
    [184, 152,  53, 141],
    [220, 165,  92, 178],
    [ 56,  54,  40,  80],
    [238,   3,  92,  27],
    [ 11,  60, 248,   3],
    [ 38, 168, 212,  33],
    [133, 251,  63, 118],
    [206,  89, 147, 189],
    [134,  49, 187,   5],
    [106, 126,  20, 205],
    [  4,  18,  57, 175],
    [127, 103, 169, 197],
    [ 31,  40, 218, 155],
    [166,   7, 200, 253],
    [ 94,  60, 102,  98],
    [123,  69, 192,  33],
    [133, 166, 210,  98],
    [123, 158,  90, 149],
    [241,  23,  73,  91],
    [211,  70, 111,  42],
    [184, 130, 195, 157],
    [234, 251, 175,  75],
    [229,   3, 106, 195],
    [ 83, 233, 115, 247],
    [138,  36, 194,  53],
    [ 48, 144,  39, 165],
    [171, 190,  97,  55],
    [255, 115,  13,  99],
    [146, 133, 215, 246],
    [ 99, 132, 246,  45],
    [ 29,   8, 148,  23],
    [147, 121, 116, 136],
    [182, 118, 152, 133],
    [199, 132,  72, 150],
    [215,   8, 187, 144],
    [155,  67, 250, 204],
    [237, 130,  92, 253],
    [ 94, 119, 227, 246],
    [ 99,  72,   4,  25],
    [196, 115,   3,  62],
    [ 13,  82,  98,  52],
    [217, 118,   9, 185],
    [  5, 191, 233,  85],
    [132, 198, 240, 172],
    [ 89,  68, 149, 213],
    [ 41,  80,  16, 168],
    [218, 112, 126, 255],
    [145, 130, 161, 177],
    [ 30, 216, 231, 116]
], dtype=int)
# fmt: on


def gf_add(a: int, b: int) -> int:
    """GF(2^8) addition"""
    if a != a & 0xFF:
        raise ValueError("a is not a valid GF(2^8) element")
    if b != b & 0xFF:
        raise ValueError("b is not a valid GF(2^8) element")
    return a ^ b


def gf_sub(a: int, b: int) -> int:
    """GF(2^8) subtraction"""
    # Subtraction is the same as addition in GF(2^8)
    return gf_add(a, b)


def gf_mul(a: int, b: int) -> int:
    """GF(2^8) multiplication"""
    if a != a & 0xFF:
        raise ValueError("a is not a valid GF(2^8) element")
    if b != b & 0xFF:
        raise ValueError("b is not a valid GF(2^8) element")

    if a == 0 or b == 0:
        return 0
    log_a = LOG_TABLE[a]
    log_b = LOG_TABLE[b]
    # Ensure the result is in the range [0 to P**M - 2]
    log_result = (log_a + log_b) % (P**M - 1)
    return int(EXP_TABLE[log_result])


def gf_inv(a: int) -> int:
    """GF(2^8) multiplicative inverse"""
    if a != a & 0xFF:
        raise ValueError("a is not a valid GF(2^8) element")
    if a == 0:
        raise ZeroDivisionError("Inverse of zero is undefined in GF(2^8)")

    log_a = LOG_TABLE[a]
    # Ensure the result is in the range [0 to P**M - 2]
    log_result = (-log_a) % (P**M - 1)
    return int(EXP_TABLE[log_result])


def gf_div(a: int, b: int) -> int:
    """GF(2^8) division"""
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
    return int(EXP_TABLE[log_result])


def rs_enc(msg: np.typing.NDArray[np.integer]):
    """Reed-Solomon encoding for RS(68, 64)"""
    if len(msg) != K - S:
        raise ValueError(f"Message length must be {K - S}, got {len(msg)}")

    parity = np.zeros(T * 2, dtype=np.int64)
    for i in range(T * 2):
        s = 0
        for j in range(K - S):
            s ^= gf_mul(msg[j], G[j, i])
        parity[i] = s
    return parity


if __name__ == "__main__":
    print("Log table of GF(2^8): ")
    print(LOG_TABLE)

    print("\nExp table of GF(2^8): ")
    print(EXP_TABLE)

    print("\nGenerator matrix G of RS(68, 64): ")
    print(G)
