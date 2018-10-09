package com.flagcollection;

import com.facebook.react.bridge.NativeModule;
import com.facebook.react.bridge.ReactApplicationContext;
import com.facebook.react.bridge.ReactContext;
import com.facebook.react.bridge.ReactContextBaseJavaModule;
import com.facebook.react.bridge.ReactMethod;
import com.facebook.react.bridge.Callback;

import android.util.Base64;
import android.util.Log;

public class ValidateFlag3 extends ReactContextBaseJavaModule {
  private static final String[] compositeKey = new String[]{
    "hUZAf9gFIARRFTAvKRDs8A==", "gp9jPELztMsd51Ih81gO0Q=="
  };  
  private static final String flag3 = "RJ9qOOqa7pAinT19vyuQRHOGSi3FnPW5La0BYb4tnw==";
    
  public ValidateFlag3(ReactApplicationContext reactContext) {
    super(reactContext);
  }
  
  @Override
  public String getName() {
    return "ValidateFlag3";
  }
  
  public byte[] getKey () {
    byte[] parts0 = Base64.decode(compositeKey[0], Base64.NO_WRAP);
    byte[] parts1 = Base64.decode(compositeKey[1], Base64.NO_WRAP);
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
    for (int i = 0; i < encryptedFlag.length; i++){
      int keyOffset = i % key.length;
      encryptedFlag[i] = (byte) (encryptedFlag[i] ^ key[keyOffset]);
    }
    Boolean valid = flag3.equals(Base64.encodeToString(encryptedFlag, Base64.NO_WRAP));
    callback.invoke(valid);
  }
}