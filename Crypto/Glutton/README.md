# CHALLENGE_TITLE

## Category
Cryptography

## Estimated difficulty
Easy

## Description
Flag is encrypted using two byte XOR, easy to bruteforce

## Scenario
  Do you really want to eat that?
  It doesn't look like a hash brown to me.

## Write-up
The given file is a pure binary with no specific indication.
We're told that the file doesn't look like a hash, and, indeed, it doesn't fit most hash algorithms.
We can keep looking in that direction, closest to hashes still in cryptography is encryption.
Giving this to any XOR solver (such as Cyber Chef's) with a key length of 2, and a known plaintext of CSC, the flag appears.

## Solve script
[Click to see solution](https://gchq.github.io/CyberChef/#recipe=From_Hex('Auto')XOR_Brute_Force(2,100,0,'Standard',false,true,false,'CSC')&input=MGQxYyAwZDM0IDdmMjkgMTExNiAyMTFhIDExN2MgN2E3OCAxMTIyIDdkMTAgMzc3ZiAzYjdlIDIyMTAgMmM3YyAxMTI2IDdmN2UgMzM)

## Flag
CSC{1f_YoU_347_m3_y0u1l_b3_i11}

## Creator
Théo Davreux

## Creator bio
*insert dancing blobcat*
