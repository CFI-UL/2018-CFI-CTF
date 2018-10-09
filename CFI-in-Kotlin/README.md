# CFI-in-Kotlin

> mobile

Author: [sagold](https://github.com/Sag0ld)

Q-Q-Q-Q-uack?
CFI has is first mobile Apppp!
Try to get his se-se-se-cret
Try to be M-M-Me
To wi-n-n-n... Experieeence?
QUACKKKK!


## Writeup

For the CFI-in-Kotlin challenge,
you need a tool to extract data from cfi-event.apk
You can use jadx or apktool to extract your data, but I prefer jadx for his simplicity.

``` bash
jadx -d cfi-event cfi-event.apk
```

When you're done extracting the .apk, you can navigate into your folder to find the source code.
If you are use to mobile application, the standard package name always begin with:
> com.<company-name>.<app-name>.

With that being said, it's easy to find the main source code.

There, we see something that we're not use to. Extracting apk is rarely clean as when we develop an application.
- Kotlin have many feature to reduce the number of code we write.
- jadx split inner classes and anonymous classes into <class-name>$<method-name>$<number>.

method-name: refer to the method containing anonymous or innerClass.
number: is to specified which class it's.

Whit that being said, in this challenge we see LoginActivity and InformationActivity as mainClass.

As the challenge description say, « Try to be Me »,  we can assume that we need to do something related to the creator.
Like we said earlier we have a LoginActivity... ~~Odd isn't it ?~~

If we read the LoginActivity, we can find some errors of extracting data, but you can also see the logic behind the app.
And most important, variable! We have dummy credential!

> Email: alerionMascot@CFIUL.com
> Password: HappyFirstYear

With those email and password you can maybe... be the creator!?

Now, install the cfi-event app in you emulator or phone. (You can see in the androidManisfest.xml file which version you need to run the app.)
Let's sign in with the cred we found in the LoginActivity.

With a internet connection, the flag will appear under the CFI logo.

> Flag: CFI{DOUMMY_creeeeeddddd_issSoFriENDlieee_QUACKKKK}

I hope you liked this challenge.
