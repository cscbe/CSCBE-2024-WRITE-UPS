import '../helper.dart';

final condition = [
  i.ci(0, 1),
  i.ci(1, 1),
  i.cr(2, 0),
  i.su(2, 1),
  i.jn(2, 8),
  i.ci(4, 89),
  i.op(4, 0),
  i.jz(2, 8),
  i.st(),
];
