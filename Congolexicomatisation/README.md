# Congolexicomatisation

Me and my friends are testing out that new crypto system.
It is RSA based but use that super duper prime number generator made by the first congolese scholar.
Just like Eddy Malou, this prime generator repeats itself, **a lot**. Maybe too much for cryptographic applications?

In order to make sure it's secure, I encrypted 50 variants of our secret message using 50 public keys.
Can you find the two vulnerable keys, retrieve their private key and decrypt their message?

> crypto

## Setup

If you want to generate random challenge, randomize the seed.
1. Run challenge.py to generate 50 ciphers and their 50 public keys
2. Zip the challenge folder and upload it. Two of the public keys share a prime. Which one does is random.
For the current seed, it is key35 and key39

## Writeup

We are provided with many cipher texts and the public keys used to encrypt them.
There is a good hint in the challenge description stating that the number generator repeats itself.
If it repeats primes used in the keypair, we can break two keys that share this repeated prime.
By using the Euclidean algorithm for GCD (greater common divisor), if we find two factors between two public keys modulus that are not `1`, we definitively know that they share this prime.

We load all modulus into an array and try to find a GCD that is not one. Pretty fast, we find this prime that is used in key35 and key39

`230017159194752100203407138276965345342141092280537395159590297592543645444449`

By dividing both modulus by this prime, we find the respective other prime. From there, we just have to generate a new keypair to find both private keys.

We decrypt both messages and find the flag, padded with random characters.

`CFI{yo_mama_never_told_you_to_use_decent_prng_boy??}`

