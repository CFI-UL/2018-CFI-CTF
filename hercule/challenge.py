#!/usr/bin/python3
import math
import random
from typing import List

ENDIAN = "big"

ASCII = "ASCII"
BLOCK_SIZE = 4
PUBLIC_EXPONENT = 65537

KEY_BITS = 54 // 2
MILLER_RABIN_ROUNDS = 60


class PublicKey:
    def __init__(self, e, m):
        self.exponent = e
        self.modulus = m
        print(f"Public key created : exp={e}, modulus={m}")


class PrivateKey:
    def __init__(self, d, m):
        self.secret = d
        self.modulus = m
        print(f"Private key created : secret={d}, modulus={m}")


def miller_rabin(n, rounds):
    # Implementation uses the Miller-Rabin Primality Test
    # The optimal number of rounds for this test is 40
    # See http://stackoverflow.com/questions/6325576/how-many-iterations-of-rabin-miller-should-i-use-for-cryptographic-safe-primes
    # for justification

    # Taken from https://gist.github.com/Ayrx/5884790

    # If number is even, it's a composite number

    if n == 2:
        return True

    if n % 2 == 0:
        return False

    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(rounds):
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def egcd(a, b):
    x, y, u, v = 0, 1, 1, 0
    gcd = 0
    while a != 0:
        q, r = b // a, b % a
        m, n = x - u * q, y - v * q
        b, a, x, y, u, v = a, r, u, v, m, n
        gcd = b
    return gcd, x, y


def genKeyPair(p: int, q: int) -> (PublicKey, PrivateKey):
    modulus = p * q
    phi = (p - 1) * (q - 1)
    _, d, _ = egcd(PUBLIC_EXPONENT, phi)
    d = d % phi
    if d < 0:
        d += phi
    public_key = PublicKey(PUBLIC_EXPONENT, modulus)
    private_key = PrivateKey(d, modulus)
    return public_key, private_key


def chunkify(string: str):
    """Create a generator of chunks of CHUNK_SIZE length"""
    for i in range(0, len(string), BLOCK_SIZE):
        yield string[i:i + BLOCK_SIZE]


def split_and_pad(string: str) -> List[bytes]:
    # Rough implementation of PKCS#5

    bytes_list = [bytes(substring, encoding=ASCII) for substring in chunkify(string)]
    if len(bytes_list[-1]) == BLOCK_SIZE:
        # The string is exact size so we must add a whole block
        bytes_list.append(bytes([BLOCK_SIZE] * BLOCK_SIZE))
    else:
        last_block = bytearray(bytes_list[-1])
        missing_bytes = BLOCK_SIZE - len(last_block)
        last_block.extend(bytearray([missing_bytes] * missing_bytes))
        bytes_list[-1] = bytes(last_block)

    return bytes_list


def unpad_and_decode(decrypted_bytes: List[bytes]) -> str:
    last_block = decrypted_bytes[-1]
    if last_block[-1] == BLOCK_SIZE:
        assert len(last_block) == BLOCK_SIZE
        # Means the last block is full padding
        decrypted_bytes = decrypted_bytes[:-1]
    else:
        # Only the last block have padding
        bytes_to_remove = last_block[-1]
        decrypted_bytes[-1] = last_block[:-bytes_to_remove]
    decrypted_strings = [str(bytes_to_convert, encoding=ASCII) for bytes_to_convert in decrypted_bytes]
    return "".join(decrypted_strings)


def encrypt(text: str, public: PublicKey) -> List[int]:
    padded_bytes = split_and_pad(text)
    return [_encrypt(octets, public) for octets in padded_bytes]


def decrypt(encrypted: List[int], private: PrivateKey) -> str:
    decrypted_bytes = [_decrypt(cipher_int, private) for cipher_int in encrypted]
    decrypted_string = unpad_and_decode(decrypted_bytes)
    return decrypted_string


def _encrypt(text_bytes: bytes, public: PublicKey) -> int:
    cipher_text = pow(int.from_bytes(text_bytes, byteorder=ENDIAN, signed=False), public.exponent, public.modulus)
    return cipher_text


def _decrypt(encrypted: int, private: PrivateKey) -> bytes:
    decrypted_value: int = pow(encrypted, private.secret, private.modulus)
    decrypted_byte = decrypted_value.to_bytes(BLOCK_SIZE, byteorder=ENDIAN, signed=False)
    # solved_text = str(unhexlify(hex(decrypted_value)[2:]), encoding=ASCII)
    return decrypted_byte


def bruteforce(modulus: int) -> (int, int):
    radius = math.floor(math.sqrt(modulus))
    if radius % 2 == 0:
        radius -= 1
    while radius >= 3:
        if modulus % radius == 0:
            assert (modulus // radius) * radius == modulus
            print(f"Found a factorisation : {modulus//radius} * {radius} = {modulus}")
            return modulus // radius, radius
        radius -= 2


def generatePQ() -> (int, int):
    p = random.randint(2 ** KEY_BITS, 2 ** (KEY_BITS + 1) - 1)
    q = random.randint(2 ** KEY_BITS, 2 ** (KEY_BITS + 1) - 1)
    while not miller_rabin(p, MILLER_RABIN_ROUNDS):
        p = random.randint(2 ** KEY_BITS, 2 ** (KEY_BITS + 1) - 1)
    while not miller_rabin(q, MILLER_RABIN_ROUNDS):
        q = random.randint(2 ** KEY_BITS, 2 ** (KEY_BITS + 1) - 1)
    print(f"Generated key from p={p} and q={q}")
    return p, q


if __name__ == "__main__":
    #p, q = generatePQ()
    p = 235811647
    q = 226997873
    pub, priv = genKeyPair(p, q)
    bruteforce(pub.modulus)
    cipher = encrypt("""CFI{there_is_a_good_reason_why_rsa_keys_are_huge}""", pub)
    print(cipher)
    solved = decrypt(cipher, priv)
    print(solved)
