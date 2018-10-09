import logging
from base64 import a85encode, a85decode
from typing import List

STEPS_AMT: int = 13

logging.getLogger(__name__).setLevel(logging.DEBUG)


def step_encode(text_string: str):
    text_bytes: bytes = bytes(text_string, encoding="ascii")
    a85_bytes: bytearray = a85encode(text_bytes)
    logging.debug(f"Encoded : {a85_bytes}")
    encoded_bytes_array: List(int) = [_steps_up(byte) for byte in a85_bytes]
    encoded_bytes = bytes(encoded_bytes_array)
    logging.debug(f"Encoded + shifted : {encoded_bytes}")
    return str(encoded_bytes, encoding="ascii")


def step_decode(text_string: str):
    encoded_bytes = bytes(text_string, encoding="ascii")
    logging.debug(f"Sanity : {encoded_bytes}")
    decoded_bytes_array = [_steps_down(byte) for byte in encoded_bytes]
    decoded_bytes = bytes(decoded_bytes_array)
    logging.debug(f"Decoded + unshifted : {decoded_bytes}")
    text_bytes = a85decode(decoded_bytes)
    return str(text_bytes, encoding="ascii")


def _steps_up(byte: int):
    return ((byte - 33 + STEPS_AMT) % 85) + 33


def _steps_down(byte: int):
    return ((byte - 33 - STEPS_AMT) % 85) + 33


def badstep(byte):
    return (byte - STEPS_AMT) % 85


if __name__ == "__main__":
    futureflag = """Early binary repertoires include Bacon's cipher, Braille, International maritime signal flags, and the 4-digit encoding of Chinese characters for a Chinese telegraph code (Hans Schjellerup, 1869). Common examples of character encoding systems include Morse code, the Baudot code, the American Standard Code for Information Interchange (ASCII) and Unicode.
Morse code was introduced in the 1840s and is used to encode each letter of the Latin alphabet, each Arabic numeral, and some other characters via a series of long and short presses of a telegraph key. Representations of characters encoded using Morse code varied in length.
The Baudot code, a five-bit encoding, was created by Emile Baudot in 1870, patented in 1874, modified by Donald Murray in 1901, and standardized by CCITT as International Telegraph Alphabet No. 2 (ITA2) in 1930.
Fieldata, a six- or seven-bit code, was introduced by the U.S. Army Signal Corps in the late 1950s. 
    
    Here is a flag for you : CFI{ascii85_is_more_space_efficient_than_mere_base64_encoding}"""

    encoded = step_encode(futureflag)
    print(f"Encoded flag : {encoded}")
    decoded = step_decode(encoded)
    print(f"Verified : {decoded}")

    print(f"Step 1 : {bytes(a85decode(encoded))}")
    temp = [_steps_down(byte) for byte in bytes(encoded, encoding="ascii")]
    print(f"Step 2 : {a85decode(bytes((temp)))}")
