# Sili-con Carne

## Category
Reversing

## Estimated difficulty
Extreme

## Description
A handmade virtual machine, of which only the source of a few programs, notes, and binaries are shared.

The idea is that the person will recover binary instructions using the provided source, then the shorter programs, then bigger programs.

The last program, "challenge.bin", decrypts a built in string to the flag.

This can either be done by hand (but extremely impractical), or by reimplementing the VM themselves, which would be the idea.

## Scenario
We found a delapidated laboratory under a decrepit restaurant kitchen, apparently formerly squatted by a long time POI.

It's got it all: rusty disks, destroyed computers, and contraband microcontrollers being manufactured.

We've been hoping to find this guy's password for ever, but he's always used his own designs to keep us off his chips.

And old laptop was amongst the rubble, but we only managed to extract a few files before it burst in flames, a bunch of source files, binaries, and one note.

Can you somehow find his password amongst all of this?


## Write-up
See attached Writeup.md

## Solve script
Have [Dart](https://dart.dev/) installed.
go into Challenge/Private
run `dart pub get`
run `dart run bin/solve.dart <PATH_TO_FILE>` replacing the path with the path to the challenge.bin


## Flag
CSC{ROASTEDCORN}

## Creator
Théo Davreux

## Creator bio
Too dangerous with a computer, I'm just sharing the load of the suffering I cause. Sorry.