# Forever remembered - missed

## Category
Cryptography

## Estimated difficulty
Easy

## Description
challenge using base64 and binary encoding with substitution of numbers in binary 0,1 -> 1,2

## Scenario
A close friend recently passed away, a note was found nearby, we would like you to figure out what it says.

## Write-up
estimated time: 2 minutes
this challenge can be solved using cyberchef using the recipe
- SUB(01) replacing 1 and 2 with 0 and 1 respectively; using find/replace twice works too
- From Binary converting the binary string to text
- From Base64 converting the base64 encoded string to the raw string

a similar solution implemented in python can be found in Resources/POC.py

## Solve script
static challenge, no health check required, solution script can be found in Resources/POC.py
static challenge, no health check required, solution script can be found in Resources/POC.py

## Flag
CSC{in_memory_of_a_dear_friend_I_will_miss_you}

## Creator
Kenzo Staelens

## Creator bio
I'm a former CSC participant, there's not much interesting about me. I hope you enjoyed the challenge