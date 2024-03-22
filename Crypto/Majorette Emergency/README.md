# Majorette Emergency

## Category
Cryptography

## Estimated difficulty
Easy

## Description
Given an md5hash of a rockyou password which protects the flag, recover the flag

## Scenario
  I'm late for my cheerleading class, and I can't get my flags out of this awful lockbox!
  I remember I wrote how to open it in my diary, but I can't even read my own handwriting!
  What am I gonna do...

## Write-up
When opening the diary, we're greeted by a suite of 32 characters.

If we use any hash identifier, it'll tell us it's most likely MD5.

If we either use hashcat with rockyou, or any public rainbow table service, we get the password, `Use_A_Key`, and we can recover the flag.

## Solve script
N/A

## Flag
CSC{N0t_v3ry_57urdy_15_it_N0w}

## Creator
Théo Davreux

## Creator bio
ONE TWO CSC WILL JUST BEAT YOU
THREE FOUR I DONT KNOW WHAT TO SAY, HO!
