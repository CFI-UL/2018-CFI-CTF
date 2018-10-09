# powerPacked

> reverse

Author: [jorkanofaln](https://github.com/jorkanofaln)

a packed powerpc 32bit compiled using anti-debugging


## Setup

Add challenge to the challenge repository

## Writeup

Open the binary in Hopper Disassembler in order to reverse engineer it.

Try to find the _main_ function.

Since the main function, doesn't exist scroll at the bottom of the disassembly page to find the packer used to obfuscate/pack the binary.

Then unpack the binary using the `upx -d` command.

Open the unpacked binary in Hopper.

Go to the _main_ function

Continue Analyzing the dissambled code 

find the the `0xffffe` number

substract it to the first string

There you have the flag! `CFI{i_love_powerpc}`

