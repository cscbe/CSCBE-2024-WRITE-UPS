import '../helper.dart';

// Check if reg0 works
// Set all registers to a specific bit
// Add them all together
// Check = 255
// And now, RAM test
// Write 255, Read and compare
// Write 170, Read and compare
// Write 85 , Read and compare
// Write 0  , Read and compare
// If all is ok, output ascii 0
final memtest = <int>[
  i.jn(0, 4),
  i.ci(0, 255),
  i.jz(0, 4),
  i.jn(0, 7),
  i.ci(0, 49),
  i.op(0, 0),
  i.st(),
  i.ci(1, 1),
  i.ci(2, 2),
  i.ci(3, 4),
  i.ci(4, 8),
  i.ci(5, 16),
  i.ci(6, 32),
  i.ci(7, 64),
  i.ci(8, 128),
  i.ci(9, 2),
  i.ci(10, 4),
  i.ci(11, 8),
  i.ci(12, 16),
  i.ci(13, 32),
  i.ci(14, 64),
  i.ci(15, 128),
  i.ad(1, 2),
  i.ad(1, 3),
  i.ad(1, 4),
  i.ad(1, 5),
  i.ad(1, 6),
  i.ad(1, 7),
  i.ad(1, 8),
  i.su(1, 0),
  i.jn(1, 4),
  i.ci(1, 1),
  i.ad(1, 9),
  i.ad(1, 10),
  i.ad(1, 11),
  i.ad(1, 12),
  i.ad(1, 13),
  i.ad(1, 14),
  i.ad(1, 15),
  i.su(1, 0),
  i.jn(1, 4),
  // Write 255
  i.ci(0, 255),
  i.ci(1, 0),
  i.ci(2, 1),
  i.wr(1, 0), // 44
  i.ad(1, 2), // 45
  i.jn(1, 44), // 46
  // Read and compare
  i.rr(3, 1), // 47
  i.ad(1, 2), // 48
  i.su(3, 0), // 49
  i.jz(1, 53), // 50
  i.jn(3, 4), // 51
  i.jz(3, 47), // 52
  // Write 170
  i.ci(0, 170), // 53
  i.ci(1, 0), // 54
  i.ci(2, 1), // 55
  i.wr(1, 0), // 56
  i.ad(1, 2), // 57
  i.jn(1, 56), // 58
  // Read and compare
  i.rr(3, 1), // 59
  i.ad(1, 2), // 60
  i.su(3, 0), // 61
  i.jz(1, 65), // 62
  i.jn(3, 4), // 63
  i.jz(3, 59), // 64
  // Write 85
  i.ci(0, 85), // 65
  i.ci(1, 0), // 66
  i.ci(2, 1),
  i.wr(1, 0),
  i.ad(1, 2),
  i.jn(1, 68), // 70
  // Read and compare
  i.rr(3, 1),
  i.ad(1, 2),
  i.su(3, 0),
  i.jz(1, 77),
  i.jn(3, 4),
  i.jz(3, 71),
  // Write 0
  i.ci(0, 0), // 77
  i.ci(1, 0),
  i.ci(2, 1),
  i.wr(1, 0),
  i.ad(1, 2),
  i.jn(1, 80),
  // Read and compare
  i.rr(3, 1),
  i.ad(1, 2),
  i.su(3, 0),
  i.jz(1, 89),
  i.jn(3, 4),
  i.jz(3, 83),
  i.ci(0, 48), // 89
  i.op(0, 0),
  i.st()
];
