# Chinese_Food

I've sent a few of my friends the secret location of my birthday party. I really don't want the evil Eve to come and crash the party you see.
I sure hope it was a good idea to send the message without any *padding* or *armoring*.

The three messages are the same. Find a way to retrieve the message without breaking the key. (You can try to break the key if you want, but chances are against you :D)

> crypto

## Setup

If you want to generate random challenge, randomize the seed.

Run challenge.py to generate 3 ciphers and their 3 public keys
Zip the challenge folder and upload it. The message is the same in all cipher.

## Writeup

The challenge tells us that all messages are the same, without any armoring.
Furthermore, our public exponent is 3 and we have 3 messages.
This is probably vulnerable to the Chinese Remainder Attack.

The theorem states that provided you have `n` coprime divisor (the public moduli) and `n` remainder, you can find the base which satisfies the system for all cases.

This means that by having 3 copies of the same message, encrypted with 3 different public key using 3 as the public exponent, we can decrypt the message.

This is mostly mathematical, but using the implementation from https://mail.python.org/pipermail/edu-sig/2001-August/001665.html, we can find the value of message^3.
We then only need to find the cube root of the integer to find the decrypted value of the block.

Since the numbers are big, we can use this simple algorithm to find the integer part of the root as we know it's a perfect cube.
```python
def root(x,n):
     """Finds the integer component of the n'th root of x,
     an integer such that y ** n <= x < (y + 1) ** n.
     """
     high = 1
     while high ** n < x:
         high *= 2
     low = high/2
     while low < high:
         mid = (low + high) // 2
         if low < mid and mid**n < x:
             low = mid
         elif high > mid and mid**n > x:
             high = mid
         else:
             return mid
     return mid + 1```

We then obtain the integer value of the hex encoded ASCII. We can retrieve the original message by doing
`bytearray.fromhex(hex(value)[2:]).decode()

And we get b'Good job, here is your flag : CFI{this_is_the_reason_we_either_armor_our_message_or_dont_use_3_as_the_public_exponent}. Want a side of dumpling with it?\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c'

