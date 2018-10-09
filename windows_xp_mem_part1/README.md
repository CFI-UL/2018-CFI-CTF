# Windows_XP_mem_part_1

> forensics

Author: [jorkanofaln](https://github.com/jorkanofaln)

A Windows XP SP3 memory capture with some secrets.


## Writeup

Use `tar -xvf memSecret.tar.xz` to extract the memory capture file

Use the volatility to find out which profile to use: `volatility imageinfo -f winxpMem.mem`

```
Output:
Volatility Foundation Volatility Framework 2.6
INFO    : volatility.debug    : Determining profile based on KDBG search...
          Suggested Profile(s) : WinXPSP2x86, WinXPSP3x86 (Instantiated with WinXPSP2x86)
                     AS Layer1 : IA32PagedMemoryPae (Kernel AS)
                     AS Layer2 : FileAddressSpace (/home/jorkano/Data/winxpMem.mem)
                      PAE type : PAE
                           DTB : 0x334000L
                          KDBG : 0x80545ae0L
          Number of Processors : 1
     Image Type (Service Pack) : 3
                KPCR for CPU 0 : 0xffdff000L
             KUSER_SHARED_DATA : 0xffdf0000L
           Image date and time : 2018-05-20 21:32:21 UTC+0000
     Image local date and time : 2018-05-20 17:32:21 -0400

Use the notepad plugin to extract the image's secrets:
Output:
Volatility Foundation Volatility Framework 2.6
Process: 3740
Text:
Ask Commander Shepperd for help
Steal a clone, from a rich and powerful person
Here is my secret:
Volatility Foundation Volatility Framework 2.6
Process: 3740
Text:
?

Text:
d

Text:


Text:
?

Text:
Ask Commander Shepperd for help
Steal a clone, from a rich and powerful person
Here is my secret:
CFI{Notepad_0riana_secret_is_ins3cur3}
```

There you have the flag! `CFI{Notepad_0riana_secret_is_ins3cur3}`
