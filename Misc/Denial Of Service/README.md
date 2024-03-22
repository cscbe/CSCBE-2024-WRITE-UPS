# Denial Of Service

## Category
Misc

## Estimated difficulty
Easy

## Description
DOS header of calc.exe has been changed to decode & print the flag when the executable is executed in a DOS emulator like DOSBOX. The assembly can also be manually reversed, but the fact the challenge is not categorized as a reversing challenge might help the contestant conclude there's an easier way to solve it.

## Scenario
My grandpa gave me this calculator application. He told me he used this executable all the time to print out his precious flag. I can't seem to find anything. Must be a Denial Of Service.

## Write-up

The challenge title & description hint that the challenge has something to do with DOS (Denial Of Service) & is old (grandpa). For backwards compatibility, the PE file structure includes a DOS (Disk Operating System) header (also called MS-DOS header), which is a 64 byte structure containing some file metadata and a DOS stub. This DOS stub is a piece of assembly that only gets executed when the program is loaded on [MS-DOS](https://nl.wikipedia.org/wiki/MS-DOS). In most modern-day applications, this DOS stub contains a standard piece of code which prints out: `This program cannot be run in DOS mode.`. Looking at the executable of this challenge in a hex editor shows that the DOS stub has been modified. This could also be found by doing a diff (find different bytes) between the executable in this challenge and the standard Windows calc.exe.

No readable text seems to be present in the new DOS stub. One way to solve the challenge could be to disassemble the opcodes and reverse the decoding process of the flag. This challenge isn't tagged as a reversing challenge however. Another way to solve it is to use an MS-DOS emulator like [DOSBOX](https://www.dosbox.com/).

Mounting the directory from which DOSBOX was launched as a new drive (C:), changing to this new drive, and running the executable can be accomplished with the following commands, leading to the flag.
```
mount c: .
c:
calc.exe
```

## Flag
CSC{I_can_rUn_In_D0S_m0De!}

## Creator
Idea: Romain Jennes
Implementation: Alex Van Mechelen

## Creator bio
Romain & Alex are former contestants from the team Royal Military Hackademy. They hope you'll have a great time solving their challenge!
