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

// console.log(validateFlag2("CFI{obfuscated_javascript_is_not_secured}"));

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
