import 'dart:typed_data';

import '../helper.dart';

final helloImmediate = [
  0x3048,
  0x7000,
  0x3045,
  0x7000,
  0x304C,
  0x7000,
  0x304C,
  0x7000,
  0x304F,
  0x7000,
  0x3020,
  0x7000,
  0x3043,
  0x7000,
  0x3053,
  0x7000,
  0x3043,
  0x7000,
  0xFFFF
];

final helloImmediateAsm = [
  i.ci(0, 0x48),
  i.op(0, 0),
  i.ci(0, 0x45),
  i.op(0, 0),
  i.ci(0, 0x4C),
  i.op(0, 0),
  i.ci(0, 0x4C),
  i.op(0, 0),
  i.ci(0, 0x4F),
  i.op(0, 0),
  i.ci(0, 0x20),
  i.op(0, 0),
  i.ci(0, 0x57),
  i.op(0, 0),
  i.ci(0, 0x4F),
  i.op(0, 0),
  i.ci(0, 0x52),
  i.op(0, 0),
  i.ci(0, 0x4C),
  i.op(0, 0),
  i.ci(0, 0x44),
  i.op(0, 0),
  i.st(),
];
