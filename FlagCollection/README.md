# FlagCollection 🚩

> mobile

Author: [lilc4t](https://github.com/masterT)

Simple mobile application that allow you to submit valid flags to your collection. You can only submit 3 flags the moment.


## Setup

### Development

Check out the [React Native documentation](https://facebook.github.io/react-native/).

### Build

Build the APK:

```shell
$ src/android/gradlew assembleRelease -p src/android/
```

This generates `src/android/app/build/outputs/apk/release/app-release.apk`.

```shell
$ mv src/android/app/build/outputs/apk/release/app-release.apk FlagCollection.apk
```

## Writeup

A good place to start is to run the application on your device or the Android emulator that is shipped with [Android Studio](https://developer.android.com/studio/).

To install the APK in your emulator or on your _connected_ device:

```
adb install FlagCollection.apk
```

When you open the application we see the CFI logo and an empty list of flag. There is `"Submit flag"` button that open a modal box from where you can submit a flag. When you press the `"Submit" `button in the modal box we'll see the message `"Invalid flag! Try harder!"`. These strings will help us navigate through the source code.

Now decompile the APK using [jadx](https://github.com/skylot/jadx).

```
$ jadx -d decompiled FlagCollection.apk
```

This will create the directory `decompiled` with `resources` and `sources` directories:

```
$ tree -L 2 decompiled/
decompiled/
├── resources
│   ├── AndroidManifest.xml
│   └── res
└── sources
    ├── android
    ├── bolts
    ├── com
    ├── javax
    ├── okhttp3
    ├── okio
    └── org

10 directories, 1 file
```

If you open `decompiled/resources/AndroidManifest.xml` you'll see the reference to the application code.

```xml
<!-- ... -->
<application android:theme="@style/AppTheme" android:label="@string/app_name" android:icon="@mipmap/ic_launcher" android:name="com.flagcollection.MainApplication" android:allowBackup="false">
    <!-- ... -->
</application>
<!-- ... -->
```

In this case it's `com.flagcollection.MainApplication`. The namespace is `com.flagcollection`. Here are the files that belong to this namespace:

```
$ ls -1  decompiled/sources/com/flagcollection
BuildConfig.java
MainActivity.java
MainApplication.java
R.java
ValidateFlag3.java
ValidateFlag3Package.java
```

Let's check the source code of the `MainApplication`.

When can see the `MainApplication` implements the `ReactApplication` from the package [com.facebook.react.ReactApplication](https://github.com/facebook/react-native/blob/master/ReactAndroid/src/main/java/com/facebook/react/ReactApplication.java). So the application is a React Native. It means it bundle JavaScript code and execute it from the Java code. More information [here](https://www.reactnative.guide/3-react-native-internals/3.1-react-native-internals.html).

Let's find the JavaScript code. For that we need to decompress the APK. Since an APK file is just Zip archive you can unzip it!

```
$ file FlagCollection.apk
FlagCollection.apk: Zip archive data, at least v2.0 to extract
```

```
$ unzip FlagCollection.apk -d unarchived
```

The JavaScript code is located at `unarchived/assets/index.android.bundle`. It's minified so let's un-minified it using [js-beautify](https://www.npmjs.com/package/js-beautify).

```
$ js-beautify -s 2 -f unarchived/assets/index.android.bundle -o index.js
```

This generate the file `index.js` using an indentations of 2 spaces.

Let's search some of the key strings we noted.

String: `Invalid flag! Try harder!`

```
$ grep -n -i 'Invalid flag! Try harder!' index.js
23890:            t ? (n.ToastAndroid.show('Good job!', n.ToastAndroid.SHORT), l.props.onSubmitSuccess(e), l.hideModal()) : n.ToastAndroid.show('Invalid flag! Try harder!', n.ToastAndroid.SHORT), l.setState({
```

Line 23890.

Let read the code arround the line 23890.


```js
l.submitFlag = function() {
  var e = l.state.flag;
  (0, i.validateFlag)(e).then(function(t) {
    t ? (n.ToastAndroid.show('Good job!', n.ToastAndroid.SHORT), l.props.onSubmitSuccess(e), l.hideModal()) : n.ToastAndroid.show('Invalid flag! Try harder!', n.ToastAndroid.SHORT), l.setState({
      flag: ''
    })
  })
}
```

Let's refactor the code.

```js
l.submitFlag = function() {
  var flag = l.state.flag;
  (0, i.validateFlag)(flag)
    .then(function (valid) {
      if (valid) {
        n.ToastAndroid.show('Good job!', n.ToastAndroid.SHORT)
        l.props.onSubmitSuccess(flag)
        l.hideModal()
      } else {
        n.ToastAndroid.show('Invalid flag! Try harder!', n.ToastAndroid.SHORT)
      }
      l.setState({flag: ''})
    })
}
```

It call a function `validateFlag` and that returns a Promise, then it it resolve with a true value it display `"Good job!"` otherwise it display `"Invalid flag! Try harder!"`. Let's find the definition of this function.

Can't find it in the context, [Babel](https://babeljs.io/) transpiled code is to messed up. Let's grep the code.

```
$ grep -n 'validateFlag' index.js
23889:          (0, i.validateFlag)(e).then(function(t) {
23964:  }), r.validateFlag = function(n) {
```

It looks like it's defined at the line 23964.

```js
r.validateFlag = function(n) {
  return c(n).then(function(e) {
    return !!e || [a, f].some(function(e) {
      return e(n)
    })
  })
};
```

Refactored:

```js
// n -> flag
r.validateFlag = function (flag) {
  // c -> validation1
  return validation1(flag)
    .then(function(e) {
      if (e) {
        return true
      } else {
        // a -> validation2
        // f -> validation3
        return [validation2, validation3].some(function (validation) {
          return validation(flag)
        })  
      }
    })
};
```

So it calls the function `validation1` (previously `c`) with the argument `flag` (previously `n`) that returns a Promise, then if it resolve with a positive value, it return `true`, otherwise, it return if the functions `validation2` and `validation3` (previously `a` and `f`) returned a `true` value with the `flag`.

Just below the function there is the tree function `c`, `a` and `f`. Let's check them one by one.


## Flag 1

```js
function c(n) {
  return new Promise(function(e) {
    i.NativeModules.ValidateFlag3.validate(n, function(n) {
      e(n)
    })
  })
}
```

Refactored:

```js
function validation1 (flag) {
  return new Promise(function (resolve) {
    i.NativeModules.ValidateFlag3.validate(flag, function (valid) {
      resolve(valid)
    })
  })
}
```

It looks like it uses [NativeModules](https://facebook.github.io/react-native/docs/native-modules-ios) which allows to call native code (in this case Java code) from JavaScript. It calls the `validate` methods of the native module `ValidateFlag3`.

Native modules are added in `MainApplication.java`. Indeed there is a package `ValidateFlag3Package`.

```java
// ...
protected List<ReactPackage> getPackages() {
    return Arrays.asList(new ReactPackage[]{new MainReactPackage(), new ValidateFlag3Package()});
}
// ...
```

Now let's take a look to `ValidateFlag3Package.java`.

```java
// ...
public class ValidateFlag3Package implements ReactPackage {
    public List<ViewManager> createViewManagers(ReactApplicationContext reactContext) {
        return Collections.emptyList();
    }

    public List<NativeModule> createNativeModules(ReactApplicationContext reactContext) {
        List<NativeModule> modules = new ArrayList();
        modules.add(new ValidateFlag3(reactContext));
        return modules;
    }
}
```

It add the module `ValidateFlag3`. Let's open `ValidateFlag3.java`.

```java
// ....
public class ValidateFlag3 extends ReactContextBaseJavaModule {
    private static final String[] compositeKey = new String[]{"hUZAf9gFIARRFTAvKRDs8A==", "gp9jPELztMsd51Ih81gO0Q=="};
    private static final String flag3 = "RJ9qOOqa7pAinT19vyuQRHOGSi3FnPW5La0BYb4tnw==";

    public ValidateFlag3(ReactApplicationContext reactContext) {
        super(reactContext);
    }

    public String getName() {
        return "ValidateFlag3";
    }

    public byte[] getKey() {
        byte[] parts0 = Base64.decode(compositeKey[0], 2);
        byte[] parts1 = Base64.decode(compositeKey[1], 2);
        byte[] key = new byte[parts0.length];
        for (int i = 0; i < parts1.length; i++) {
            key[i] = (byte) (parts0[i] ^ parts1[i]);
        }
        return key;
    }

    @ReactMethod
    public void validate(String flag, Callback callback) {
        byte[] key = getKey();
        byte[] encryptedFlag = flag.getBytes();
        for (int i = 0; i < encryptedFlag.length; i++) {
            encryptedFlag[i] = (byte) (encryptedFlag[i] ^ key[i % key.length]);
        }
        Boolean valid = Boolean.valueOf(flag3.equals(Base64.encodeToString(encryptedFlag, 2)));
        callback.invoke(valid);
    }
}
```

Bingo we found the `validate` method. Let's see what we have here. It call `getKey` and set the `flag` bytes in variable `encryptedFlag`. Then it performs on each byte of the given `flag` (set as `encryptedFlag`) a [XOR](https://en.wikipedia.org/wiki/XOR_gate) using the operator [^](https://docs.oracle.com/javase/specs/jls/se7/html/jls-15.html#jls-15.22.2). Finally it compares the base64 value of the `encryptedFlag` with the static constant `flag3`.

So to retrieve the flag we need to XOR `flag3` with the `key`.

The `getKey` method initialize a buffer of byte `key`, takes each part of the `compositeKey` and decode the base64 value in `parts0` and `parts1`. Then it performs on each byte of `parts0` a XOR and set the result at the byte position in the buffer `key`. Finally it returns `key`.

So to generate the `key` when need to XOR `compositeKey[0]` with `compositeKey[1]`.

You can use [cryptii](https://cryptii.com/bitwise-calculator) or other tool online to do it.

But first we need to get the hexadecimal value from base64 of those strings, you can use https://kt.gy/tools.html or other tool online.

```
flag3
(base64) RJ9qOOqa7pAinT19vyuQRHOGSi3FnPW5La0BYb4tnw==
(hexadecimal) 44 9f 6a 38 ea 9a ee 90 22 9d 3d 7d bf 2b 90 44 73 86 4a 2d c5 9c f5 b9 2d ad 01 61 be 2d 9f

compositeKey[0] 
(base64) hUZAf9gFIARRFTAvKRDs8A==
(hexadecimal) 85 46 40 7f d8 05 20 04 51 15 30 2f 29 10 ec f0

compositeKey[1] 
gp9jPELztMsd51Ih81gO0Q==
(hexadecimal) 82 9f 63 3c 42 f3 b4 cb 1d e7 52 21 f3 58 0e d1

key = compositeKey[0] ^ compositeKey[1] 
(base64) B9kjQ5r2lM9M8mIO2kjiIQ==
(hexadecimal) 07 d9 23 43 9a f6 94 cf 4c f2 62 0e da 48 e2 21

flag = flag3 ^ key
(base64) Q0ZJe3Bsel9ub19zZWNyZXRfaW5famF2YV9jb2RlfQ==
(hexadecimal) 43 46 49 7b 70 6c 7a 5f 6e 6f 5f 73 65 63 72 65 74 5f 69 6e 5f 6a 61 76 61 5f 63 6f 64 65 7d
(ascii) CFI{plz_no_secret_in_java_code}
```

There we have the first flag! 


## Flag 2

Now let's go back to the JavaScript code and take a look at the function `validation2` (previous `a`).

```js
function a(n) {
  return o.Buffer.from('Q0ZJe2Jhc2U2NF9pc19ub3Rfc2VjdXJlfQ==', 'base64').toString('ascii') === n
}
```

Refactored:

```js
function validation2 (flag) {
  return o.Buffer.from('Q0ZJe2Jhc2U2NF9pc19ub3Rfc2VjdXJlfQ==', 'base64').toString('ascii') === flag
}
```

It looks like it that the string `Q0ZJe2Jhc2U2NF9pc19ub3Rfc2VjdXJlfQ==`, and decode the base64 value and then compare it with the `flag`. So we just need to decode the string to get the flag.

You can use https://kt.gy/tools.html or other tool online.

```
(base64) Q0ZJe2Jhc2U2NF9pc19ub3Rfc2VjdXJlfQ==
(ascii) CFI{base64_is_not_secure}
```

Yeah we have to second flag!


## Flag 3

Now let's go back a last time and take a look at the last function `validation3` (previous `f`).

```js
function f(n) {
  for (var e = [], t = 2, r = 0; r < n.length; r++) {
    1 & r ? t += 13 : t -= n.length % 9;
    var u = n.charCodeAt(r) + t;
    e.push(u)
  }
  return '64,80,78,141,124,124,123,151,144,141,134,166,146,158,148,172,158,192,166,197,176,204,190,210,209,201,206,229,204,232,228,246,220,253,234,245,258,268,250,262,282' === e.join(',')
}
```

Refactored:

```js
function validation3 (flag) {
  var buffer = []
  var something = 2
  for (var i = 0; i < flag.length; i++) {
    if (1 & i) {
      something += 13
    } else {
      something -= flag.length % 9
    } 
    var value = flag.charCodeAt(i) + something;
    buffer.push(value)
  }
  return '64,80,78,141,124,124,123,151,144,141,134,166,146,158,148,172,158,192,166,197,176,204,190,210,209,201,206,229,204,232,228,246,220,253,234,245,258,268,250,262,282' === buffer.join(',')
}
```

Let's reverse the function:

```js
var codes = '64,80,78,141,124,124,123,151,144,141,134,166,146,158,148,172,158,192,166,197,176,204,190,210,209,201,206,229,204,232,228,246,220,253,234,245,258,268,250,262,282'.split(',').map(function (i) {
  return parseInt(i)
})

var flag = ''
var something = 2
for (var i = 0; i < codes.length; i++) {
  // Is odd?
  if (1 & i) {
    something += 13
  } else {
    // Flag length is the codes length.
    something -= codes.length % 9
  }
  var character = String.fromCharCode(codes[i] - something)
  flag += character
}

console.log(flag)
// CFI{obfuscated_javascript_is_not_secured}
```

Awesome we have the last flag! 
