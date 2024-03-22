# Shapeshifter

## Category
Reversing

## Estimated difficulty
Hard

## Description
Contestant has to discover this is a polymorphic executable that encrypts its "print_flag" function with a random XOR key on each runtime. When this XOR key doesn't equal the specific value `0x0101010101010101`, the opcodes of the print_flag function are changed in a way that the flag is no longer printed out. The challenge can either be solved statically or through patching the executable.

Build with:
```
gcc -o legendary_binary polymorphic_easy.c
```
NOW RUN THE BINARY AT LEAST ONCE BEFORE HANDING IT TO THE CONTESTANT
> Since it prints out the flag on first execution
```
./legendary_binary
./legendary_binary
```

The binary included in the `Public` folder of this challenge zip is ready to be handed out to the contestants.

## Scenario
Legend says this binary only prints out the flag on its first execution.
I had to try it!
It's true!
...but now the flag is gone, and the binary seems to be changing form on every execution.
Can you recover the flag?

## Write-up
When running the program, it prints out `My opcodes have changed! No flag anymore...`
The challenge description hints the binary changes on every execution. This can be verified by taking a hash (ex: md5sum) of the binary before and after an execution.

The next question you can ask is which part(s) of the executable are changing. After comparing two versions of the executable, you find two parts of the binary that change:

 1. The value of the `key` parameter in the `.data` section.
 2. The content (opcodes) of the `print_flag()` function.

Note how the opcodes of the `print_flag()` function make no sense at all -> It is probably encrypted in some way and gets decrypted at runtime before execution. To figure out where this happens you can use a decompiler of your choice. You'll notice the `mutate()` function gets called just before the `print_flag()` function.

Inside the `mutate()` function, the `key` variable from the `.data` section gets used as an XOR key on the encrypted content of the `print_flag()` function. One could thus manually XOR the opcodes in the encrypted `print_flag()` function with the `key` variable from the `.data` section to get the actual opcodes of the `print_flag()` function and reverse this assembly to get the flag.

Alternatively, you find a way to make the program print out the flag. Remember how when running the program it doens't print out the flag, but rather `My opcodes have changed! No flag anymore...` This means the opcodes of the `print_flag()` function get changed after decryption. Inside the `mutate()` function, there is an if-statement that checks whether the `key` parameter in the `.data` section equals `0x0101010101010101`. Since this is (most likely) not the case, the opcodes inside the `print_flag()` function get XORed with the value of the `xor_key` parameter in the `.data` section, making the `print_flag()` function print out something else than the flag. By patching the executable to invert the if-condition, the flag is printed out on execution.

Alternatively, instead of patching the if-condition, you could zero out the contents of the `xor_key` parameter in the `.data` section.

PS: Remember how the challenge description states the binary only prints out the flag on its first execution. This is because on first execution, the `key` variable from the `.data` section is still equal to `0x0101010101010101`, but as soon as the program gets executed, the new key is randomly generated (on each execution) and only has a tiny chance of being equal to `0x0101010101010101`.

## Flag
csc{S3lf_m0d!fy1ng_4S53mbly_1s_b3aut1ful!}

## Creator
Alex Van Mechelen

## Creator bio
Alex is a master student polytechnics at the Royal Military Academy. He is former contestant from the teams Royal Military Hackademy & DIG174L. He hopes you'll have a great time solving his challenges!
