# CHALLENGE_TITLE
Blockchain

## Category
Cryptography

## Estimated difficulty
Medium

## Description
Offline challenge about PBKDF2. PBKDF2 has easy collisions due to its contruction. Challengers need to recover the hash of the string used for PBKDF, which is leaked in the hash of the previous block.

## Scenario
You secrets are exposed ! Blockchain is unsecure ! Meet the new crypto revolution, the most innovative crypto venture of the century, a once-in-a-lifetime opportunity that will make you rich: the private blockchain ! It is so secure and will protect you from any scam or hacker, even password bruteforcing, thanks to our disruptive technology.

## Write-up
The blocks are encrypted with a key derived using PBKDF2. PBKDF2 has the [property](https://en.wikipedia.org/wiki/PBKDF2#HMAC_collisions) that `PBKDF2(m) = PBKDF2(H(m))` when `m` is long enough.

In this challenge, `m` is the concatenation of the previous block (previous hash and data in plain) with the secret. This is exactly how the hash of that block is computed, so it gives us `H(m)`. Instead of computing the key with `m`, we can compute it from `H(m)` and decrypt the block. We repeat for each block until we get all of the characters of the flag.

The first block can't be decrypted like the others, but the character must be `C` because of the flag format.

## Solve script
`Resources/solve_blockchain.py`

## Flag
`CSC{crYPtO_M3ANs_CRYPTo6r@pHy}`

## Creator
Romain Jennes

## Creator bio
I'm a former contestant from the team Royal Military Hackademy, and I hope to help you discover the great realm of cryptography !
