# Automated Reversing

> reverse

Author: [corb3nik](https://github.com/Corb3nik)

I have 1009 binaries for you to reverse. Shouldn't take you that long right?

Have fun!

## Writeup

This challenge required participants to reverse about 1000 binaries.

The key to this challenge is the fact that all of the binaries have the same structure, making it easy for us to automate the reversing process.


### Reversing a binary
Let's take a look at a binary. Here I'm using `objdump` on OSX.

```
$ objdump -d binary0 --x86-asm-syntax=intel

binary0:        file format ELF64-x86-64

Disassembly of section .shellcode:
.shellcode:
  6000b0:       6a 00   push    0
  6000b2:       6a 05   push    5
  6000b4:       48 89 e7        mov     rdi, rsp
  6000b7:       48 c7 c0 23 00 00 00    mov     rax, 35
  6000be:       0f 05   syscall
  6000c0:       58      pop     rax
  6000c1:       58      pop     rax
  6000c2:       48 8b 44 24 10  mov     rax, qword ptr [rsp + 16]
  6000c7:       8a 10   mov     dl, byte ptr [rax]
  6000c9:       80 f2 57        xor     dl, 87
  6000cc:       80 fa 5d        cmp     dl, 93
  6000cf:       75 10   jne     16 <.shellcode+0x31>
  6000d1:       48 c7 c7 00 00 00 00    mov     rdi, 0
  6000d8:       48 c7 c0 3c 00 00 00    mov     rax, 60
  6000df:       0f 05   syscall
  6000e1:       48 c7 c7 01 00 00 00    mov     rdi, 1
  6000e8:       48 c7 c0 3c 00 00 00    mov     rax, 60
  6000ef:       0f 05   syscall
  6000f1:       00  <unknown>
```

The first lines of this binary calls syscall #35, which is `nanosleep`.
You can find syscall definitions here : http://blog.rchapman.org/posts/Linux_System_Call_Table_for_x86_64/.
```
  6000b0:       6a 00   push    0
  6000b2:       6a 05   push    5
  6000b4:       48 89 e7        mov     rdi, rsp
  6000b7:       48 c7 c0 23 00 00 00    mov     rax, 35
  6000be:       0f 05   syscall
```

Then, we are taking the first character located at `[rsp+16]` and moving it into `dl`:

```
  6000c2:       48 8b 44 24 10  mov     rax, qword ptr [rsp + 16]
  6000c7:       8a 10   mov     dl, byte ptr [rax]
```

To figure out what is located at `[rsp+16]`, we can run it through a debugger and
find out. At `0x6000c2`, the stack looks like the following :

```
rsp       => argc
rsp + 8   => argv[0]
rsp + 16  => argv[1]
```

Therefore, we are moving the first char of argv[1] into the `dl` register.

We are then running the `xor` operation on `dl` and the number `87` :

```
  6000c9:       80 f2 57        xor     dl, 87
```

The result of that operation is checked against the number 93 :
```
  6000cc:       80 fa 5d        cmp     dl, 93
```

Depending on the result above, the binary will exit with return code 0 or 1:

```
  6000cf:       75 10   jne     16 <.shellcode+0x31>
  6000d1:       48 c7 c7 00 00 00 00    mov     rdi, 0
  6000d8:       48 c7 c0 3c 00 00 00    mov     rax, 60
  6000df:       0f 05   syscall
  6000e1:       48 c7 c7 01 00 00 00    mov     rdi, 1
  6000e8:       48 c7 c0 3c 00 00 00    mov     rax, 60
  6000ef:       0f 05   syscall
```

By convention, a successful exit status is `0`. Therefore, our goal is to figure out
which input
The goal is to find which input will result in an exit status of 0.

Based on our example above, to obtain the exit status of 0, we need to solve the
following equation : `dl ^ 87 = 93`. We can reverse the operation :

```
>>> 93 ^ 87
10
```

The answer here is 10, which is a newline in ascii.

### Reversing 1000 binaries

Upon reversing 2/3 binaries, you'll notice that each binary follows the same
structure.

In each binary, only three elements will differ :

- The operation to use (xor, sub or add)
- The 2nd operand of the operation : `xor dl, random_number_here`
- The final check : `cmp dl, some_number`

Knowing this, we can create a script in order to determine the value of `dl` to use
for each binary :

```
#!/usr/bin/env python

flag = ""
for i in xrange(970):
    path = "binaries/binary{}".format(i)
    print i
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
```

By concatenating the `dl` value of each binary, we obtain the flag :

```
$ python solution.py

Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. The flag is CFI{1s_th1s_4_pr0g_ch4ll_0r_4_r3ve3se_ch4ll?}. Aenean vulputate eleifend tellus. Aenean leo ligula, porttitor eu, consequat vitae, eleifend ac, enim. I stole this idea directly from Defcon Quals 2016. Phasellus viverra nulla ut metus varius laoreet. Quisque rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper ultricies nisi. Nam eget dui. Etiam rhoncus. Maecenas tempus, tellus eget condimentum rhoncus, sem quam semper libero, si
```
