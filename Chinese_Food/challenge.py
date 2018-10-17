#!/usr/bin/python3
import logging
import os
import random
import string

from functools import reduce

from operator import mul, add
from typing import List, Tuple

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
# Locking seed to generate challenge
#random.seed(13277027826014293874669876764081272619701015982741852941173235834562422745824849756056632621460193043425602)
ENDIAN = "big"
FLAG = """flag-hVIHlhtt37S4UfCGCmTaUGxK8iucwFmz"""

ASCII = "ASCII"
BLOCK_SIZE = 60
PUBLIC_EXPONENT = 3

# KEY_BITS = 512 // 2
KEY_BITS = 512 // 2

MILLER_RABIN_ROUNDS = 60


class PublicKey:
    def __init__(self, e, m):
        self.exponent = e
        self.modulus = m
        logging.debug(f"Public key created : exp={e}, modulus={m}")

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, PublicKey):
            if self.exponent == other.exponent:
                return self.modulus == other.modulus
        return False

    def __str__(self):
        """Return the public key as text"""
        return f"Public key\nPublic exponent : {self.exponent}\nModulus : {self.modulus}"


class PrivateKey:
    def __init__(self, d, m):
        self.secret = d
        self.modulus = m
        logging.debug(f"Private key created : secret={d}, modulus={m}")

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, PrivateKey):
            if self.secret == other.secret:
                return self.modulus == other.modulus
        return False


class KeyPair:
    def __init__(self, pair: Tuple[PublicKey, PrivateKey]):
        self.public = pair[0]
        self.private = pair[1]


def generatePQ() -> (int, int):
    p = random.randint(2 ** KEY_BITS, 2 ** (KEY_BITS + 1) - 1)
    q = random.randint(2 ** KEY_BITS, 2 ** (KEY_BITS + 1) - 1)
    while not miller_rabin(p, MILLER_RABIN_ROUNDS):
        p = random.randint(2 ** KEY_BITS, 2 ** (KEY_BITS + 1) - 1)
    while not miller_rabin(q, MILLER_RABIN_ROUNDS):
        q = random.randint(2 ** KEY_BITS, 2 ** (KEY_BITS + 1) - 1)
    logging.debug(f"Generated key from p={p} and q={q}")
    return p, q


def generateListPQ() -> (List[int], List[int]):
    p = list()
    q = list()
    i = 0
    while i < 3:
        new_p, new_q = generatePQ()
        if new_p not in p and new_p not in q and new_q not in q and new_q not in p:
            p.append(new_p)
            q.append(new_q)
            i += 1
    return p, q


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


def crt(modulos_list: List[int], remainders_list: List[int]) -> int:
    """
    TAKEN FORM https://mail.python.org/pipermail/edu-sig/2001-August/001665.html
    Chinese Remainder Theorem:
    ms = list of pairwise relatively prime integers
    as = remainders when x is divided by ms
    (ai is 'each in as', mi 'each in ms')

    The solution for x modulo M (M = product of ms) will be:
    x = a1*M1*y1 + a2*M2*y2 + ... + ar*Mr*yr (mod M),
    where Mi = M/mi and yi = (Mi)^-1 (mod mi) for 1 <= i <= r.
    """

    M = reduce(mul, modulos_list)  # multiply ms together
    Ms = [M // mi for mi in modulos_list]  # list of all M/mi
    ys = [egcd(Mi, mi)[1] for Mi, mi in zip(Ms, modulos_list)]  # uses inverse,eea
    return reduce(add, [ai * Mi * yi for ai, Mi, yi in zip(remainders_list, Ms, ys)]) % M


def find_invpow(x: int, n: int) -> int:
    """
    Finds the integer component of the n'th root of x,
    an integer such that y ** n <= x < (y + 1) ** n.
    """
    BASE = 2
    upper_bound = 1
    exponent = 0
    while upper_bound ** n < x:
        exponent += 1
        upper_bound = BASE ** exponent
    lower_bound = pow(2, exponent-1)
    candidate = lower_bound
    while lower_bound < upper_bound:
        candidate = (lower_bound + upper_bound) // 2
        if lower_bound < candidate and candidate ** n < x:
            lower_bound = candidate
        elif upper_bound > candidate and candidate ** n > x:
            upper_bound = candidate
        else:
            assert candidate ** n == x
            return candidate
    assert (candidate + 1) ** n == x
    return candidate + 1


def egcd(a, b):
    oldB = b
    x, y, u, v = 0, 1, 1, 0
    gcd = 0
    while a != 0:
        q, r = b // a, b % a
        m, n = x - u * q, y - v * q
        b, a, x, y, u, v = a, r, u, v, m, n
        gcd = b
    return gcd, x % oldB, y


def gcd(a: int, b: int) -> int:
    if b > a:
        return gcd(b, a)

    if a % b == 0:
        return b

    return gcd(b, a % b)


def randomAscii():
    random_length = random.randint(50, 100)
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(random_length))


def generateCiphersAndKey(public_list: List[PublicKey]) -> List[List[int]]:
    cipher_list = []
    os.makedirs("./challenge", exist_ok=True)
    for i, public_key in zip(range(100), public_list):
        with open(f"./challenge/cipher{i}", "w") as f:
            cipher = encrypt(f"Good job, here is your flag : {FLAG}. Want a side of dumpling with it?", public_key)
            logger.debug(f"Encrypted sequence : {cipher}")
            cipher_list.append(cipher)
            f.write(str(cipher))
        with open(f"./challenge/key{i}", "w") as f:
            f.write(str(public_key))
    logging.info("Generated challenges")
    return cipher_list


def _verify_length(cipher_list):
    temoin = len(cipher_list[0])
    for items in cipher_list:
        if temoin != len(items):
            return False
    return True


def chineseRemainderAttack(public_list, cipher_list):
    decrypt_list = []
    assert _verify_length(cipher_list)
    assert len(public_list) == len(cipher_list)
    factor_list = []
    for key in public_list:
        product_value = reduce(lambda x, y: x.modulus * y.modulus, public_list[1:])
        factor_list.append(product_value * egcd(product_value, key.modulus)[1])
    for i in range(len(cipher_list[0])):
        cipher_numbers = [cipher[i] for cipher in cipher_list]
        modulozz = [key.modulus for key in public_list]
        message_integer = find_invpow(crt(modulozz, cipher_numbers), public_list[0].exponent)
        message = message_integer.to_bytes(BLOCK_SIZE, byteorder=ENDIAN, signed=False)
        decrypt_list.append(message)
    return b''.join(decrypt_list)


if __name__ == "__main__":
    p_list, q_list = generateListPQ()
    public_list = list()
    private_list = list()
    for i, p, q in zip(range(100), p_list, q_list):
        pub, priv = genKeyPair(p, q)
        public_list.append(pub)
        private_list.append(priv)

    cipher_list = generateCiphersAndKey(public_list)
    solved = chineseRemainderAttack(public_list, cipher_list)

    logging.debug(solved)
