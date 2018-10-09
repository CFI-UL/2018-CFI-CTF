import { NativeModules } from 'react-native';
import { Buffer } from 'buffer'

function validateFlag1 (flag) {
  const encryptedFlag = 'Q0ZJe2Jhc2U2NF9pc19ub3Rfc2VjdXJlfQ=='
  const decryptedFlag = Buffer.from(encryptedFlag, 'base64').toString('ascii')
  return  decryptedFlag === flag
}

function validateFlag2 (flag) {
  const isOdd = (number) => (number & 1)
  let encryptedFlag = []
  let change = 2
  for (var i = 0; i < flag.length; i++) {
    if (isOdd(i)) {
      change += 13
    } else {
      change -= (flag.length % 9)
    }
    let value = flag.charCodeAt(i) + change
    encryptedFlag.push(value)
  }  
  return encryptedFlag.join(',') === '64,80,78,141,124,124,123,151,144,141,134,166,146,158,148,172,158,192,166,197,176,204,190,210,209,201,206,229,204,232,228,246,220,253,234,245,258,268,250,262,282'
}

function validateFlag3 (flag) {
  return new Promise((resolve) => {
    NativeModules.ValidateFlag3.validate(flag, (valid) => {
      resolve(valid)
    })
  })
}

export function validateFlag (flag) {
  return validateFlag3(flag)
    .then((valid) => {
      if (valid) return true
      return [validateFlag1, validateFlag2].some((validationFunction) => {
        return validationFunction(flag)
      })
    })
}