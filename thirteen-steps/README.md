# thirteen-steps

> crypto

Author: [enteris](https://github.com/Enteris)

Thirteen steps : Drinking like it's nineteen-ascii-85\
I know I need to do something thirteen times, but what could it be? All I have is a bunch of bytes...which also seem encoded

```
DGPA^T(1_>QVV_?8RQ2ANaQ%?O$hq88QTl4P!+F/8MFYUQs:)Q8Ps96O\-@E8MG7dO$2a+<=V[2SPsX>MILA2QVVL5Q;;V.SQBa48RZD=QVVL5N'5%tS/NTOQVn$@O\*HP<`3_;O$#W<QVha)O$D^8QrG8gO]QL)S5UW5O\](!M*-G3S.95BRgrqBCfY>\NaZR7SPsF/OC2S/OUbs4NDg$@EDLPd8O6pmP>c@,NaQ(A<=Ug9?RI@J8MP4nQ<eHDNb2e0R9F798R5"DM)jG#MG\P"Rgr)?M*T%$QW56BU0&5JQ=1uCQVhY7NDg$eQsa'>8PsK0NY&+TO\*H^MIU8.SIT5@NDhHDSQ9B;C0P>_O#5_u8O7N"QVq=*N=JCeNDg$)Qs^+$QW.t:Q;;\0Qs:huQXXU>M)jGtOAd?CB-b:OEYfp"QVn#!QWIb.NDhN0F$T3&NXfX1NDg%:MI@^7QXX'HNFQO&N=Ka58RcG;8KT!A=^`MSQVn$5S.9bUN_$(7Qj!c<M*T%u8Q/,#OUc93SRQ6D8R5"DSQ9B;F\d1dQO[N5R8!guNaaVTN_a5k8M>1cMcXI(QXas:RnmpE8Pa;-8RZVINXf'BO\-@9M)jG#MG\P"RpdMUO"!9%8RZ8DO#HL;QrG9;Qs=?>MHja-S5sXASIT\PNaZ(5S.9PB8P^PDN`o("Rnm(08Qf]C<t834R9'[?N`-a-SQBg?S.9PB8Ps5&RnmV/NaQ!DN`-.*NDjF'SmcEDO:F'rRpfrDM*T%u8Ru>CO#Gs,O$B3=N`-;3OW4d#O\*H^MIU8.SIT5@NDhHDM@O<*T2RDDO$#W<QVha)O$D^D8R)DE8PsT4MIL4#8PjbJDHgnaNXeIWSl0RA8QTkF=sc7T<=W&LSPsL@N_$',QOYf&?m74;Q<d+.N&otr8PjbJC-^+\Pu8flSmZZ?T(1tJ8KT$>=rJTbQVn$?SPO3,MI9%%UJkc=Me=5mCc>Cc8PaJCEa3djRp9I:O$M$,Pm$itPuDD/MH'%3C0GY_MGRr!8N^!:8K]3sE^D-?;@[KO8KT$A=W@j2O#H7#MIK(<8P^PCO%H@]Qs^,NNaue3<_!SF8PsK0NY&+WMI@^7QXX'HNFQO&N=KL98RcG;8OG1%<t7U0Q=hD3O#ZI$Pm$6mRpL5OO$B3EO\*I3MIL44=sl7SS/`_O8IcqY1CbUC8M(4nNXfj;8P^P6Ptt+.N'QjAU0VtW@g(qgEbS$rM)seG?;54JLf+l2N_OY,MG[#bN`9\tM)sY$SP=:4MHjSuNaQLuMbeJu?Qrp]QVha)O$D_@
```

Here are some interesting reads: 
 - https://en.wikipedia.org/wiki/Caesar_cipher
 - https://en.wikipedia.org/wiki/Ascii85


## Setup

- Create a new _virtualenv_ to preserve your python installation.
- Install the dependencies with `pip install .`
- Simply give the string you want to encode as a parameter to the `step_encode()` function to create the encoded flag.
- You may use `step_decode()` to decode the obtained flag.

## Writeup

It would seem we have a base85 encoded string to start the challenge.
Decoding it gives us : 
> nOt\xb5\x9e\xf1\xe0\x01\x97Ot\xc2I\`g\xb9\x8e\`Z\x7f\x8fC\xe3\x0bIWp\xac\x92=\x83\x10I0c\xac\x98\\\r\x83IQk\xb9\x91J\x15\x88I0t\xaa\x

That won't do it. We have a bunch of unusual bytes here, like 97 and e0. This probably means that something happened to
 the encoded string in order to obtain our initial text. 
 
 The challenge mention thirteen, which might refers to ROT-13, a commonly used "cipher".
 
 By rotating by 13 the bytes values before we decode the ascii85...
 > ValueError: Non-Ascii85 digit found: 
 
 Oh. I guess we are out of bounds. But pray tell, what are ascii85 bounds?
 
 Reading some more about ascii85, we notice that the
 printable space is shifted by 33, in order to get characters ranging from `!` to `u`
 
 By adding the shift, we obtain : 
 >  Early binary repertoires include Bacon's cipher, Braille [...] \
 Here is a flag for you : CFI{ascii85_is_more_space_efficient_than_mere_base64_encoding}
 
 Success :D
