# hercule

They say you should never implement your own crypto algorithms.
This challenge displays one of the many implementation flaws you can find in a custom RSA.

Here is the flag. But it's encrypted with RSA. The padding algorithm is PKCS#5 with .
I'll provide you with the Public key : `Public key created : exp=65537, modulus=53528742297626831`

And here is the encrypted string : `[48944927437833612, 16618833042310571, 5184494133895961, 34925820981208595, 32624945606321423, 23493881996355757, 26922771394119503, 39459212340002548, 30566210251065891, 21336317446368629, 39157017037329648, 4769341917225250, 44809893317200587]`

Can you retrieve the secret key and decrypt the message?

> crypto

## Setup

Just run `pip install .` to install dependencies.

Then run `challenge.py` to generate an encrypted flag and the associated Public and Private keys

## Writeup

Looking at the Public key, we immediately notice the modulus is quite small for an asymmetric cryptography scheme.
We could probably bruteforce the `p` and `q` values used to create the modulus and recreate the private key.

We could use fancy factorisation algorithms like the general number field Sieve, but if the key is small enough, a simple trial division algorithm might suffice.
We use the following algorithm :

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

Using the square root saves time as we assume both number are probably of similar length which mean they must be under the square root of the result.

Quickly, the algorithm spits out the two primes factor of the modulus : `Found a factorisation : 235811647 * 226997873 = 53528742297626831`

Using those values, we can create the private key using the extended enclidian algorithm to find the modular inverse of the public exponent within the modulus

Turns out the secret is `secret=7597606795359425`. Decrypting the first value with this private key (using RSA formula `message = cipher^secret mod modulus`)
gives us the value `1128679803` which converted in hexadecimal gives `4346497b`. Decoded as ASCII we get `CFI{`, which indeed seems like the first part of the flag.

Decrypting every values gives us : `CFI{there_is_a_good_reason_why_rsa_keys_are_huge}\x03\x03\x03`. We then remove the padding and obtain our flag.

