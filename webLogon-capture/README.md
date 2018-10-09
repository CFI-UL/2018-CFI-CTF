# webLogon capture

> forensics

Author: [jorkanofaln](https://github.com/jorkanofaln)

An network capture to an insecure network 


## Writeup

Open Wireshark

Follow the the TCP Stream

Find the password field: `%20%43%46%49%7b%31%6e%73%33%63%75%72%33%5f%6c%30%67%30%6e%7d%20`

visit [https://kt.gy/tools.html](https://kt.gy/tools.html) and URL decode the password

There you have the flag! `CFI{1ns3cur3_l0g0n}`
