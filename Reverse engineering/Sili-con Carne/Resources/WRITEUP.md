Sili-con Carne is fundamentally a VM/CPU reverse engineering challenge, everything else is just in context of this idea.

The challenge provides 3 bits of information:
- The notes
- The sources
- The binaries

The notes have important stuff, but we'll come back to them as needed, the first bit of information they give is a suggested order to explore the files.

The easiest to start with is the source, as it's generally done with simple programs with few instructions.

## Hello

This is a simple hello world, looking at the source, we can quickly spot it:
```
LI 0 'H'
OP 0 0
LI 0 'E'
OP 0 0
LI 0 'L'
OP 0 0
LI 0 'L'
OP 0 0
LI 0 'O'
OP 0 0
LI 0 ' '
OP 0 0
LI 0 'W'
OP 0 0
LI 0 'O'
OP 0 0
LI 0 'R'
OP 0 0
LI 0 'L'
OP 0 0
LI 0 'D'
OP 0 0
ST
```

Looking at the Binary, it breaks down fairly similarly:

| bit | bit | str |
| ---- | ---- | ---- |
| 48 | 30 | H0 |
| 00 | 70 | .p |
| 45 | 30 | E0 |
| 00 | 70 | .p |
| 4C | 30 | L0 |
| 00 | 70 | .p |
| 4C | 30 | L0 |
| 00 | 70 | .p |
| 4F | 30 | O0 |
| 00 | 70 | .p |
| 20 | 30 | .0 |
| 00 | 70 | .p |
| 57 | 30 | W0 |
| 00 | 70 | .p |
| 4F | 30 | O0 |
| 00 | 70 | .p |
| 52 | 30 | R0 |
| 00 | 70 | .p |
| 4C | 30 | L0 |
| 00 | 70 | .p |
| 44 | 30 | D0 |
| 00 | 70 | .p |
| FF | FF | ÿÿ |

From this, we can see that "LI" = 0x30, "OP" = 0x70, and "ST" = "0xFFFF"
We can also see that instructions are always 2 bytes, the last bit of data in the source is seen as the first bit of data in the binary.

Googling "LI", it's the same as the MISP instruction "Load Immediate".
"OP" is not googleable, but the relation to the load which always is paired with 0, indicates that it outputs something.
ST is at the end of the program, but we can only guess what it is.

## hello_mem

This is the same concept as above, but this time introducing the concept of memory.

Looking at the notes, we can see that there are only 16 instructions, and ST is not a regular instruction, so we can count "17" total instructions.

The code is deceptively simple, certainly not matching the size of the binary:

```
LI 0 .STEAMEDHAMS
CP 0 183
LI 0 0
OP 0 183
ST

.STEAMEDHAMS "<cut for brevity>"
```

We already know what "LI" and "OP" are.

"CP" is named as such to indicate a parallel to the unix copy tool, it's also structured in the same way as the "OP" instruction is, with the size of the text in .STEAMEDHAMS used as a second argument. It will copy the memory in ROM to RAM.

This introduces the second mode of "OP", where it's length argument is not zero, since the text is copied to RAM, and there are no immediates where we read the value to, this has to output the string itself from RAM directly.

Looking at the program memory, we can also see everything is aligned to 16 bits, even if the text does not use all 16 bits to be stored in the ROM.

## Condition

Introduces the concept of register copy, jumps, subtraction, and instructions whose first argument is not zero.

The notes contain a rough outline of the code, but in text form, as well as the expected output, and a mention of the "And" instruction.

The code itself has fairly simple logical flow:
```
LI 0 1
LI 1 1
LR 2 0
SU 2 1
JN 2 8  ----+
LI 4 'Y'    |
OP 4 0      |
JZ 2 8  ----+
            |
ST      <---+  Line 8
```

We now have "JN" and "JZ", which are similar to existing jump instructions (JNZ and JZ) findable on google, "CR", in a similar way, exists already in MISP, and "SU", which, if the name is not obvious enough, can be understood to be subtraction with the code's context:
- JZ jumps if 2 is zero
- JN does not
- Register 2 is filled with the value of Register 0, so, 1
- An operation happens
- "Jump if not zero" does not jump, therefore, 2 is equal to zero
- Therefore, the operation must set 2 to zero, since we already have a "copy register" instruction, the only remaining option is subtraction.

Looking at the binaries, we can now see that instructions we used to know (For ex, LI as 0x30), are now not mapped exactly the same. However, they're still similar, in this case, 0x31 and 0x34.

From this, we can see that the first argument sits on the same byte as the instruction, as it's second nibble, and the first one would make sense as the one that defines the instruction, as we know we only have 16 instructions, plus ST.

We can also derive from here that we have at most 16 accessible registers, as it wouldn't be possible to specify higher registers.

We can now build a map of the instructions we have, and we don't have:

0 - CP
1 - ?
2 - ?
3 - LI
4 - LR
5 - JZ
6 - JN
7 - OP
8 - ?
9 - SU
A - ?
B - ?
C - ?
D - ?
E - ?
F - ?
FF - ST

## Loop

It's the last bit of source we have, it's a Fibonacci sequence generator, as is hinted by the notes.

We also can see that the ram is 8 bit, and instructions are packed in words.

Looking at the source, we only have one new instruction, AD, the 8th instruction.

## Life

A small introduction to sourceless exploration.

From the notes, we know exactly what is output by the program, `*`, the 42nd ASCII character.

Let's reconstruct the source from what we know:
```
CI 0 6
CI 1 7
?? 0 1
OP 0 0
ST
```

We can see Reg 0 = 6, and Reg 7 = 7
We know 0 = 42, from the notes

The only operation that transforms 6 and 7 into 42 is a multiplication, so we'll name this instruction "ML", the 11th instruction.
## memtest

A program to clearly indicate the outline of the chip's register and memory size, using basic loops.

The notes indicate the presence of overflow behavior, so the registers are expected to overflow, knowing the RAM is 8 bit, it tells us the registers are 8 bit too.

If we decode the operations into readable code, we can see that
- 0 is checked and jumps over if it works
- Registers 1 through 8, and 9 through 15 are filled with one bit in ascending order
- They're all added together and checked to see if they properly add up, we can derive that we only have 15 registers here.

There are then two loops which happen multiple times:
```
CI 0 255/170/85/0
CI 1 0
CI 2 1
?? 1 0
AD 1 2
JN 1 44
```
And
```
?? 3 1
AD 1 2
SU 3 0
JZ 1 53
JN 3 4
JZ 3 47
```

Since we've already checked the registers, only the RAM is left.
A memory test starts with writing a pattern, then reading it back and checking it's status.
So, with these two loops, we can infer that the first missing instruction Writes to RAM, while the second Reads from RAM.

Let's call them "WR" (instruction 2),  and "RR" (instruction 1).
## demo_xor

A bigger program doing some bigger memory operations.

When looking at the binary, we can see that there are two "data parts", one is readable (`HELLO!!!`) whereas the second is not.

Since this is an XOR demo, and there are no obvious keys in the code, we can assume that they're both going to be XOR'd together.

If we were to do it manually, we'd see that it outputs `GOODBYE!`

There is only one unknown instruction in this loop:

```
CI 2  16 <---+
CI 3  1      |
CI 4  8      |
RR 5  0      |
RR 6  1      |
?? 5  6      |
WR 2  5      |
AD 0  3      |
AD 1  3      |
AD 2  3      |
SU 4  3      |
JN 4  11 ----+
```

Since this is an XOR demo, and we don't have such an instruction yet, in addition to the cycle of "Reading two things, doing something to them, then writing them back", we can infer that this is XOR, or "XR", Instruction 13

## challenge

Let's look at the notes first, we can see that it mentions two additional instructions: shift left and shift right.

Here's what we know:

The ROM is handled in 16 bit words, the RAM is in 8bit bytes, the Registers are 8 bit bytes.
We have 16 registers, and 256 bytes of RAM.

We have one instruction we don't know: And, Shift Left and Shift Right.

We know these instructions:
```
0  CP A, B   -> Copy part of progmem[A...A+B] to rammem[0...0+B]
1  RR A, B   -> A = rammem[B]
2  WR A, B   -> rammem[A] = B
3  CI A, Imm -> A = Imm
4  CR A, B   -> A = B
5  JZ A, B   -> Jump to B if A is zero
6  JN A, B   -> Jump to B if A is not zero
7  OP A, B   -> Prints data either in register, or in memory address
8  AD A, B   -> A = A+B
9  SU A, B   -> A = A-B
A  ???
B  ML A, B   -> A = A*B
C  ???
D  XR A, B   -> A = A^B
E  ???
F  ???
FF ST        -> Stop
```


If we first look at all instructions in that code, we can see we're missing 3 instructions: C, E, and F, exactly the same amount as the amount of instructions we don't know, so we can forget about instruction A.

All of our missing instructions are located in this loop:
```
SU 5 4
CI 6 1
CI 7 128
?? 6 5    (C)
?? 7 5    (F)
CR 8 2
?? 8 6    (E)
JZ 8 43
AD 3 7
JN 5 34
```

We can only guess which instruction goes where, which, by hand, would make the computation extremely impractical, this is where we have no choice but to build an emulator if we want to figure it out.

Build a basic emulator of the chip we have reverse engineered until now, I recommend looking up CHIP8 emulator guides, they are fairly simple, and are usually very well documented.

You should use the existing binaries as references and test programs, as it's always trivial to know what the output is expected to be, so you can ensure your code is working properly.

Once your emulator can run all of the other code, all you have to do is run all permutations of the three instructions we have left.

Here are the expected results for all permutations: (A=And, L = Shift Left, R = Shift Right)
```
ALR: ðñðâÏ¬<ÄÆÿ88q(
ARL: ÿ0SÃv;9ÇÇ×
RLA: °ÓCö»¹GGW
RAL: 0SCv;9GGW
LRA: ÿ0SÃv;9ÇÇ×
LAR: CSC{ROASTEDCORN}
```