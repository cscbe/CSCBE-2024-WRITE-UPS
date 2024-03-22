# Additional Problems

## Category
Cryptography

## Estimated difficulty
Hard

## Description
It's a crypto challenge based around the DGHV homomorphic-encryption scheme (see e.g. https://ieeexplore.ieee.org/document/8242007). The idea behind homomorphic encryption is that you can perform operations on the plaintext through the encrypted text. For example, if you add two ciphertexts in DGHV, you get the encryption of the addition of the two plaintexts. In the real world, this type of encryption is of interest, as it allows operations on very sensitive data to be done safely on cloud infrastructure. The server script implements a variant of DGHV. When a user connects to it, they are shown an encrypted flag and have access to a limited set of encryption/addition/decryption operations with the same key.

## Scenario
Version 1.0 of our new encryption service has just launched! It is blazingly fast and uses state-of-the-art encryption. Stay tuned for version 2.0; I hear it will bring tons of improvements and security fixes.

## Write-up
To solve the challenge, teams must realise that DGHV is only partially homomorphic (as is widely documented, and as is also clear from DGHV's formulation) when a technique called bootstrapping is not applied. If you do too many additions of ciphertexts, you will get something that no longer decrypts to the sum of the plaintexts. What you get instead leaks information: the value of (p mod N), where p is the key and N is a parameter in DGHV. In vanilla DGHV, N is 2, such that (p mod N) does not leak much information; however, in the variant implemented on the server, N is configurable by the user. Hence, by doing this "addition overflow" with enough values of N, the CRT can be applied to recover p and, thus, decrypt the flag.

## Solve script
The solution technique above is implemented in [`Resources/exploit.py`](./Resources/exploit.py).

## Flag
`CSC{let5_m0v3_b00tstr4pp1ng_t0_v1.1}`

(This can be changed in the `Dockerfile`.)

## Creator
Arne Bouillon

## Creator bio
I am a PhD researcher in the field of computational mathematics at KU Leuven. As a student, I was an avid participant in CSCBE. My cybersecurity interests lie mainly within the areas of cryptography and binary exploitation.
