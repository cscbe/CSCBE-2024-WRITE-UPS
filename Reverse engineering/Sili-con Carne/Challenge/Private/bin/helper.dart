import 'dart:typed_data';

const i = Inst();

class Inst {
  const Inst();

  /// Copy memory from progmem to rammem.
  ///
  /// Progmem starts at memoryAddress, for "size" bytes
  ///
  /// Rammem is copied starting at offset zero, for "size" bytes
  int cp(int memoryAddress, int size) {
    assert(memoryAddress >= 0 && memoryAddress < 16);
    assert(size >= 0 && size < 256);
    return 0x0000 | (memoryAddress << 8) | size;
  }

  /// Read a byte from RAM at memoryAddress into outputRegister
  int rr(int outputRegister, int memoryAddress) {
    assert(outputRegister >= 0 && outputRegister < 16);
    assert(memoryAddress >= 0 && memoryAddress < 256);
    return 0x1000 | (outputRegister << 8) | memoryAddress;
  }

  /// Write a byte to RAM into memoryAddress from outputRegister
  int wr(int memoryAddress, int inputRegister) {
    assert(memoryAddress >= 0 && memoryAddress < 16);
    assert(inputRegister >= 0 && inputRegister < 256);
    return 0x2000 | (memoryAddress << 8) | inputRegister;
  }

  /// Write an immediate value to outputRegister
  int ci(int outputRegister, int immediateValue) {
    assert(outputRegister >= 0 && outputRegister < 16);
    assert(immediateValue >= 0 && immediateValue < 256);
    return 0x3000 | (outputRegister << 8) | immediateValue;
  }

  /// Copy the contents of inputRegister to outputRegister
  int cr(int outputRegister, int inputRegister) {
    assert(outputRegister >= 0 && outputRegister < 16);
    assert(inputRegister >= 0 && inputRegister < 16);
    return 0x4000 | (outputRegister << 8) | inputRegister;
  }

  /// If shouldJump==0, set PC to jumpTargetRegister*2
  int jz(int shouldJump, int jumpTargetImmediate) {
    assert(shouldJump >= 0 && shouldJump < 16);
    assert(jumpTargetImmediate >= 0 && jumpTargetImmediate < 256);
    return 0x5000 | (shouldJump << 8) | jumpTargetImmediate;
  }

  /// If shouldJump!=0, set PC to jumpTargetRegister*2
  int jn(int shouldJump, int jumpTargetRegister) {
    assert(shouldJump >= 0 && shouldJump < 16);
    assert(jumpTargetRegister >= 0 && jumpTargetRegister < 256);
    return 0x6000 | (shouldJump << 8) | jumpTargetRegister;
  }

  /// Output characters
  ///
  /// If size is 0, print the value in inputRegister
  ///
  /// Otherwise, print "size" memory values starting at inputRegister
  int op(int inputRegister, int size) {
    assert(inputRegister >= 0 && inputRegister < 255);
    assert(size >= 0 && size < 256);
    return 0x7000 | (inputRegister << 8) | size;
  }

  // Add left and right, store result in left
  int ad(int left, int right) {
    assert(left >= 0 && left < 16);
    assert(right >= 0 && right < 16);
    return 0x8000 | (left << 8) | right;
  }

  // Subtract left and right, store result in left
  int su(int left, int right) {
    assert(left >= 0 && left < 16);
    assert(right >= 0 && right < 16);
    return 0x9000 | (left << 8) | right;
  }

  // Divide left and right, store result in left
  int dv(int left, int right) {
    assert(left >= 0 && left < 16);
    assert(right >= 0 && right < 16);
    return 0xA000 | (left << 8) | right;
  }

  // Multiply left and right, store result in left
  int ml(int left, int right) {
    assert(left >= 0 && left < 16);
    assert(right >= 0 && right < 16);
    return 0xB000 | (left << 8) | right;
  }

  // Shiftleft left and right, store result in left
  int sl(int left, int right) {
    assert(left >= 0 && left < 16);
    assert(right >= 0 && right < 16);
    return 0xC000 | (left << 8) | right;
  }

  // Xor left and right, store result in left
  int xr(int left, int right) {
    assert(left >= 0 && left < 16);
    assert(right >= 0 && right < 16);
    return 0xD000 | (left << 8) | right;
  }

  // And left and right, store result in left
  int nd(int left, int right) {
    assert(left >= 0 && left < 16);
    assert(right >= 0 && right < 16);
    return 0xE000 | (left << 8) | right;
  }

  // Shiftright left and right, store result in left
  int sr(int left, int right) {
    assert(left >= 0 && left < 16);
    assert(right >= 0 && right < 16);
    return 0xF000 | (left << 8) | right;
  }

  /// Stop execution
  int st() {
    return 0xFFFF;
  }
}

List<int> writeBytesToRAM(Uint8List bytes, int offset) {
  final instructions = <int>[];

  for (final byte in bytes) {
    instructions.addAll([
      i.ci(15, byte),
      i.ci(14, offset),
      i.wr(14, 15),
    ]);
    offset++;
  }

  return instructions;
}

List<int> writeStringToRAM(String string, int offset) {
  return writeBytesToRAM(Uint8List.fromList(string.codeUnits), offset);
}

List<int> printAt(int offset, int size) {
  return [
    i.ci(15, 0),
    i.op(15, size),
  ];
}
