import 'dart:io';
import 'dart:typed_data';

/// The CPU itself
///
/// Composed of 2 memory units
///   PROGMEM, the read only, executable 16bit program memory, loaded at startup
///   RAMMEM, the dynamic, data only program memory
class Program {
  Uint16List progmem = Uint16List(256);
  Uint8List rammem = Uint8List(256);
  Uint8List registers = Uint8List(16);
  int pc = 0;

  Program(List<int> progin) {
    progmem.setAll(0, progin);
  }

  void step() {
    final opcode = Opcode(progmem[pc]);

    if (progmem[pc] == 0xFFFF) {
      throw Exception("Done");
    }

    pc = (pc + 1) & 0xFF;

    switch (opcode.instruction) {
      case Instruction.CP:
        var offset = 0;
        while (offset != opcode.regB) {
          rammem[offset] = progmem[registers[opcode.regA] + offset];
          offset++;
        }
      case Instruction.RR:
        registers[opcode.regA] = rammem[registers[opcode.regB]];
      case Instruction.WR:
        rammem[registers[opcode.regA]] = registers[opcode.regB];
      case Instruction.CI:
        registers[opcode.regA] = opcode.regB;
      case Instruction.CR:
        registers[opcode.regA] = registers[opcode.regB];
      case Instruction.JZ:
        if (registers[opcode.regA] == 0) {
          pc = opcode.regB;
        }
      case Instruction.JN:
        if (registers[opcode.regA] != 0) {
          pc = opcode.regB;
        }
      case Instruction.OP:
        if (opcode.regB == 0) {
          stdout.write(String.fromCharCode(registers[opcode.regA]));
          break;
        }

        var pointer = registers[opcode.regA];
        while (opcode.regB > 0) {
          stdout.write(String.fromCharCode(rammem[pointer]));
          pointer = (pointer + 1) & 0xFF;
          opcode.regB--;
        }
      case Instruction.AD:
        registers[opcode.regA] =
            (registers[opcode.regA] + registers[opcode.regB]) & 0xFF;
      case Instruction.SU:
        registers[opcode.regA] =
            (registers[opcode.regA] - registers[opcode.regB]) & 0xFF;
      case Instruction.DV:
        registers[opcode.regA] =
            (registers[opcode.regA] ~/ registers[opcode.regB]) & 0xFF;
      case Instruction.ML:
        registers[opcode.regA] =
            (registers[opcode.regA] * registers[opcode.regB]) & 0xFF;
      case Instruction.SL:
        registers[opcode.regA] =
            (registers[opcode.regA] << registers[opcode.regB]) & 0xFF;
      case Instruction.XR:
        registers[opcode.regA] =
            (registers[opcode.regA] ^ registers[opcode.regB]) & 0xFF;
      case Instruction.ND:
        registers[opcode.regA] =
            (registers[opcode.regA] & registers[opcode.regB]) & 0xFF;
      case Instruction.SR:
        registers[opcode.regA] =
            (registers[opcode.regA] >> registers[opcode.regB]) & 0xFF;
    }
  }
}

class Opcode {
  // IIII AAAA BBBB BBBB (B is Imm if applicable)
  Instruction instruction;
  int regA;
  int regB;

  Opcode(int opcode)
      : instruction = Instruction.values[opcode >> 12],
        regA = (opcode >> 8) & 15,
        regB = opcode & 255;

  String toString() {
    return "${instruction.name}: $regA, $regB";
  }
}

enum Instruction {
  // Memory Operations
  CP, // A, B   -> Copy part of progmem[A...A+B] to rammem[0...0+B]
  RR, // A, B   -> A = rammem[B]
  WR, // A, B   -> rammem[A] = B
  CI, // A, Imm -> A = Imm
  CR, // A, B   -> A = B
  JZ, // A, B   -> A == 0 ? pc = B*2
  JN, // A, B   -> A != 0 ? pc = B*2
  OP, // A, B   -> \
  //               B == 0? print A
  //               B != 0? print B characters in rammem, starting at A

  // MathOps, ALL registers!
  AD, // A, B -> A = A+B
  SU, // A, B -> A = A-B
  DV, // A, B -> A = A/B
  ML, // A, B -> A = A*B
  SL, // A, B -> A = A%B
  XR, // A, B -> A = A^B
  ND, // A, B -> A = A&B
  SR, // A, B -> A = A|B
}
