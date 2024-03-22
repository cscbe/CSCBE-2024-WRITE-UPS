import 'dart:io';
import 'dart:typed_data';
import 'package:args/args.dart';
import 'package:hex/hex.dart';
import 'execute.dart';
import 'programs/condition.dart';

void main() {
  final memoryIn = Uint16List(256);

  List<String> argv = Platform.executableArguments;

  if (argv.length != 1) {
    print("Usage: dart run bin/solve.dart <FILEPATH_TO_BINARY>");
  }

  final inbytes = File(argv[0]).readAsBytesSync();

  memoryIn.setAll(0, inbytes);

  final p = Program(memoryIn);

  print(HexEncoder(upperCase: true)
      .convert(Uint16List.fromList(memoryIn).buffer.asUint8List()));

  try {
    while (true) {
      p.step();
    }
  } on Exception {}
}
