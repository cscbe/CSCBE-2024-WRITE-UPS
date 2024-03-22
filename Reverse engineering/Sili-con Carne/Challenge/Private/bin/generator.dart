void genkeyold() {
  var initial = 94;
  var factor = 245;
  var q = 16; //CSC{WIERD_THING}

  while (q != 0) {
    print(initial);

    initial = (initial ^ factor) & 0xFF;
    factor = (1 + ((factor * 3) & 0xFF)) & 0xFF;
    q--;
  }
}

void genkey2old() {
  var a = 0x0F;
  var b = 0xF0;
  var c = 0x47;

  var q = 16;

  while (q != 0) {
    print(a);
    a = (a + b) & 0xFF;
    b = (a ^ b) & 0xFF;

    q--;
  }
}

final plain = "CSC{ROASTEDCORN}";
final key1 = [
  94,
  171,
  75,
  234,
  14,
  163,
  171,
  178,
  254,
  27,
  171,
  186,
  142,
  19,
  203,
  66
];
final key2 = [
  15,
  255,
  14,
  15,
  29,
  48,
  83,
  195,
  118,
  59,
  57,
  0,
  199,
  199,
  142,
  215
];

void main() {
  final plainList = plain.codeUnits;

  final firstXor = <int>[];

  for (int i = 0; i < plainList.length; i++) {
    firstXor.add(key2[i] ^ plainList[i]);
  }

  final flippedBits = <int>[];

  for (int i = 0; i < plainList.length; i++) {
    flippedBits.add(flipBits(firstXor[i]));
  }

  final secondXor = <int>[];

  for (int i = 0; i < plainList.length; i++) {
    secondXor.add(key1[15 - i] ^ flippedBits[i]);
  }

  print(plainList);
  print(firstXor);
  print(flippedBits);
  print(secondXor);
}

int flipBits(int input) {
  int output = 0;

  for (int flipindex = 0; flipindex < 8; flipindex++) {
    int flipBit = 1 << flipindex;

    if (input & flipBit != 0) {
      output = output + (0x80 >> flipindex);
    }
  }

  return output;
}
