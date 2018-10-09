# Windows XP mem part 2

> forensics

Author: [jorkanofaln](https://github.com/jorkanofaln)

Windows XP SP3 memory capture with internet explorer 8 history 


## Writeup

Use `tar -xvf` command to extract the file in the `ieSecret.tar.xz` archive

Use the volatility to find out which profile to use: `volatility imageinfo -f internetExplorer.mem`

```
Use Volatility to find the OS image version: volatility imageinfo -f internetExplorer.mem

Output:
Volatility Foundation Volatility Framework 2.6
INFO    : volatility.debug    : Determining profile based on KDBG search...
          Suggested Profile(s) : WinXPSP2x86, WinXPSP3x86 (Instantiated with WinXPSP2x86)
                     AS Layer1 : IA32PagedMemoryPae (Kernel AS)
                     AS Layer2 : FileAddressSpace (/media/jorkano/FreeAgent GoFlex Drive/Neue Ordner/internetExplorer.mem)
                      PAE type : PAE
                           DTB : 0x334000L
                          KDBG : 0x80545ae0L
          Number of Processors : 1
     Image Type (Service Pack) : 3
                KPCR for CPU 0 : 0xffdff000L
             KUSER_SHARED_DATA : 0xffdf0000L
           Image date and time : 2018-05-27 00:31:37 UTC+0000
     Image local date and time : 2018-05-26 20:31:37 -0400

Then use the Windows XP SP3 profile and use the internet explorer plugin: volatility --profile=WinXPSP2x86 iehistory -f internetExplorer.mem
Output:
Volatility Foundation Volatility Framework 2.6
**************************************************
Process: 2512 iexplore.exe
Cache type "DEST" at 0x1d8945
Last modified: 2018-05-26 20:30:24 UTC+0000
Last accessed: 2018-05-27 00:30:26 UTC+0000
URL: Administrator@https://www.google.com/url?url=https://www.theguardian.com/us&rct=j&frm=1&q=&esrc=s&sa=U&ved=0ahUKEwiKmITz5KHbAhXO2qQKHUMuCoEQFggVMAA&usg=AOvVaw0EduAwOOfzz74wHifeqwLw
**************************************************
Process: 2512 iexplore.exe
Cache type "DEST" at 0x1d8c8d
Last modified: 2018-05-26 20:30:24 UTC+0000
Last accessed: 2018-05-27 00:30:26 UTC+0000
URL: Administrator@https://www.google.com/url?url=https://www.theguardian.com/us&rct=j&frm=1&q=&esrc=s&sa=U&ved=0ahUKEwiKmITz5KHbAhXO2qQKHUMuCoEQFggVMAA&usg=AOvVaw0EduAwOOfzz74wHifeqwLw
**************************************************
Process: 2512 iexplore.exe
Cache type "DEST" at 0x1d931d
Last modified: 2018-05-26 20:30:24 UTC+0000
Last accessed: 2018-05-27 00:30:26 UTC+0000
URL: Administrator@https://www.google.com/url?url=https://www.theguardian.com/us&rct=j&frm=1&q=&esrc=s&sa=U&ved=0ahUKEwiKmITz5KHbAhXO2qQKHUMuCoEQFggVMAA&usg=AOvVaw0EduAwOOfzz74wHifeqwLw
**************************************************
Process: 2512 iexplore.exe
Cache type "DEST" at 0x23a455
Last modified: 2018-05-26 20:30:07 UTC+0000
Last accessed: 2018-05-27 00:30:08 UTC+0000
URL: Administrator@https://www.google.com/search?q=+CFI%7BH1kw3d_and_sp1ed_in_m3l@yu%7D&hl=de&gbv=2&oq=+CFI%7BH1kw3d_and_sp1ed_in_m3l@yu%7D&gs_l=heirloom-serp.3...2343.2343.0.2671.1.1.0.0.0.0.172.172.0j1.1.0....0...1ac.1.34.heirloom-serp..1.0.0.WGjpw8ohe4U
Title: CFI{H1kw3d_and_sp1ed_in_m3l@yu} - Google-Suche
**************************************************
Process: 2512 iexplore.exe
Cache type "DEST" at 0x23a89d
Last modified: 2018-05-26 20:30:07 UTC+0000
Last accessed: 2018-05-27 00:30:08 UTC+0000
URL: Administrator@https://www.google.com/search?q=+CFI%7BH1kw3d_and_sp1ed_in_m3l@yu%7D&hl=de&gbv=2&oq=+CFI%7BH1kw3d_and_sp1ed_in_m3l@yu%7D&gs_l=heirloom-serp.3...2343.2343.0.2671.1.1.0.0.0.0.172.172.0j1.1.0....0...1ac.1.34.heirloom-serp..1.0.0.WGjpw8ohe4U
Title: CFI{H1kw3d_and_sp1ed_in_m3l@yu} - Google-Suche
**************************************************
Process: 2512 iexplore.exe
Cache type "DEST" at 0x3e38f65
Last modified: 2018-05-26 20:30:18 UTC+0000
Last accessed: 2018-05-27 00:30:20 UTC+0000
URL: Administrator@https://www.googl
**************************************************
Process: 2512 iexplore.exe
Cache type "DEST" at 0x450ac65
Last modified: 2018-05-26 20:30:51 UTC+0000
Last accessed: 2018-05-27 00:30:52 UTC+0000
URL: Administrator@https://www.theguardian.com/us
Title: News, sport and opinion from the Guardian's US edition | The Guardian
```

There you have the flag! `FLAG: CFI{H1kw3d_and_sp1ed_in_m3l@yu}`


