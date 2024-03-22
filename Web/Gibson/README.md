# Gibson

## Category
Web

## Estimated difficulty
Easy

## Description
Basic JS obfuscated script that can be reversed online

## Scenario
Pretend it's 1999 and hack the Gibson!

## Write-up
Copy the javascript into https://obf-io.deobfuscate.io/ to get the following output:

```js
function c() {
  var _0x118798 = document.getElementById("username").value;
  var _0x46baf7 = document.getElementById("password").value;
  if (_0x118798 === "ZeroCool" && _0x46baf7 === "secret") {
    alert("CSC{IH4ck3dTh3G1bs0n!}");
  } else {
    alert("Access denied");
  }
}
```

## Solve script
PUT IT IN THE `Resources` FOLDER AND MENTION IT IN THE `healthcheck:` of `challenge.yml`

## Flag
CSC{IH4ck3dTh3G1bs0n!}

## Creator
Jeroen

## Creator bio
Still me.