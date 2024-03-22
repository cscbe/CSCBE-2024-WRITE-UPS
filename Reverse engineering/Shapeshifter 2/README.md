# Shapeshifter 2

## Category
Reversing

## Estimated difficulty
Extreme

## Description
This challenge builds further on the `Shapeshifter` challenge by implementing some extra features that make previous methods (that could be used on the first `Shapeshifter` challenge) unapplicable.

Build with;
```
gcc -o legendary_binary_2 polymorphic_hard.c
```
NOW RUN THE BINARY AT LEAST ONCE BEFORE HANDING IT TO THE CONTESTANT
> Since it prints out the flag on first execution
```
./legendary_binary_2
./legendary_binary_2
```

The binary included in the `Public` folder of this challenge zip is ready to be handed out to the contestants.

## Scenario
The first shapeshifter binary soon learned it was too easy for reversers like you to figure out its original message. That's why it evolved and protected itself even more, to prevent anyone from finding the flag after its first execution.
I really needed that flag, so I quickly executed the binary while it was still possible.
...but now the flag is gone.
Legend says only 1337 reversers can figure out what the binary used to print.

## Write-up
When running the program, it prints out `Can you reverse an extra layer of security?` The code is highly similar to that of the first `Shapeshifter` challenge, with a few additions making it harder to reverse.

Just like in the first `Shapeshifter` challenge, there are two parts of the binary that change on every execution:

1. The value of the `key` parameter in the `.data` section.
2. The content (opcodes) of the `print_flag()` function.

The opcodes of the `print_flag()` function are again decrypted (and afterwards encrypted) at runtime inside the `xor()` function (called in the `mutate()` function) using the `key` variable from the `.data` section as an XOR key.

Inside the `mutate()` function, there is again an if-statement that checks whether the `key` parameter in the `.data` section equals `0x0101010101010101`. This time however, the condition is the inverse of the one in the first `Shapeshifter` challenge, only changing the opcodes when the `key` equals `0x0101010101010101`. When the key is right, the `print_flag()` function is not only XORed with the `xor_key` from the `.data` section, but also with the `key` and the new `shellcode_key` from the `.data` section. This eliminates two methods that can be used to solve the first `Shapeshifter` challenge:

1. You can't just zero out the contents of the `xor_key` in the `.data` section, since this time, that `xor_key` contains useful information to make the binary print out the flag. And it's the useless message that gets printed out by default. (`Can you reverse an extra layer of security?`)
2. You also can't just invert the if-condition that checks key equality to `0x0101010101010101` since (assuming you didn't change the `key` to `0x0101010101010101` as well) would trigger the multiple XORs. The values of `key` and `shellcode_key` however are not right, thus changing the opcodes of the `print_flag()` function into invalid ones, causing a segfault.

Thus, you need to figure out the initial values of `key` and `shellcode_key` on the first run of the binary in order to solve this challenge (since you know the binary prints out the flag only on its first execution).

In order for the flag to be printed out, the multiple XORs must be executed inside the if-condition that checks whether `key` equals `0x0101010101010101`. We thus know the initial value of `key`.

Now how to find the initial value of `shellcode_key`?

Remembering from the first `Shapeshifter` challenge, the `xor_key` used to be a sparse value (lots of zero bytes). This time however, the `xor_key` has a quite repetitive pattern with a period of 8 bytes (`ghsruSto`). This might reveal the initial value of the `shellcode_key`. You can check the contents of the variables in the `.data` section with the following command:
```
objdump -d -s -j .data legendary_binary_2
```
Remember how the `xor_key` first gets XORed with both `shellcode_key` AND `key` before being XORed with the opcodes of the `print_flag()` function. Hence, to find the original value of the `shellcode_key`, it might be useful to XOR the `xor_key` with `key`. Taking the previously found pattern (`ghsruSto`) in the `xor_key` and XORing it with `0x0101010101010101`, reveals the original value of `shellcode_key`:

`0x666972737452756e` or in ASCII: `firstRun`

So now we know the original values of both `key` and `shellcode_key`. Patching the executable with `key` = `0x0101010101010101` and `shellcode_key` = `firstRun` won't work however, since before the `mutate()` function is called, the `xor()` function XORs the encrypted opcodes of the `print_flag()` function with the `key`, which (most likely) differs from `0x0101010101010101`. When patching the executable, the `key` should thus remain untouched. The if-condition that checks whether `key` equals `0x0101010101010101` should thus be inverted. Additionally, thanks to the properties of the XOR operation, the value of the `shellcode_key` can be patched in a way that even though the `key` doesn't equal `0x0101010101010101`, it acts the same as if it was.

We know that on the first execution of the binary, the `xor_key` is XORed with `0x0101010101010101` and with `firstRun`. If we can't change the value of `key`, which should equal `0x0101010101010101`, we can make `shellcode_key` equal to its original value `firstRun` XORed with `0x0101010101010101` and XORed with the current value of `key`. Having inverted the if-condition as well in the same patch, will make the binary print out the flag, making you a 1337 reverser, according to the legend.

Let's end with an example: 
Say the `key` value of the `legendary_binary_2` equals `0x0174deadbeef0174`.

You patch the binary in two places:
1. You invert the if-condition that checks whether `key` equals `0x0101010101010101`.
2. You make `shellcode_key` equal to `firstRun` XOR `0x0101010101010101` XOR `0x0174deadbeef0174` => `66 1c ad df cb bc 75 1b`

Run the patched binary and celebrate your victory!

## Flag
CSC{M4st3R1ng_s0m3_P0lymOrph!c_c0de_4_fUn}

## Creator
Alex Van Mechelen

## Creator bio
Alex is a master student polytechnics at the Royal Military Academy. He is former contestant from the teams Royal Military Hackademy & DIG174L. He hopes you'll have a great time solving his challenges!
