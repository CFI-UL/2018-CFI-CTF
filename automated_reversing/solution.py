#!/usr/bin/env python

flag = ""
for i in xrange(970):
    path = "binaries/binary{}".format(i)
    with open(path, "r") as f:
        binary = f.read()
        operator = binary[0xca]
        key = binary[0xcb]
        check = binary[0xce]

        if operator == "\xc2": # add
            flag += chr((ord(check) - ord(key)) & 0xff)

        elif operator == "\xea": # sub
            flag += chr((ord(check) + ord(key)) & 0xff)

        else:
            flag += chr(ord(check) ^ ord(key))

print flag
