/*
1. Copy cyphertext RAM: 16
2. Regenerate key: RAM 16+16=32
    void main() {
      var initial = 94;
      var factor = 245;
      var q = 16; //CSC{WIERD_THING}
      
      while(q != 0) {
        print(initial);
        
        initial = (initial ^ factor) & 0xFF;
        factor = (1 + (factor * 3)) & 0xFF;
        q--;
      }
    }
3. Reverse XOR 32+16 = 48
key[0] ^ cypher[15]
...
key[15] ^ cypher[0]

4. Flip bits 48+16=64
01234567 -> 76543210

5. Generate another key = 64+16=80
void main() {
  var a = 0x0F;
  var b = 0xF0;
  var c = 0x47;
  
  var q = 16;
  
  while(q!=0){
    print(a);
    a = (a + b)&0xFF;
    b = (b - c)&0xFF;
    c = (a ^ c)&0xFF;
    
    q--;
  }
}
6. Regular XOR = 80 + 16 = 96
key2[0] ^ cypher[0]
...
key2[15] ^ cypher[15]

7. Print
 */

import '../helper.dart';

var customKey = <int>[
  112,
  254,
  161,
  160,
  72,
  85,
  83,
  247,
  246,
  213,
  29,
  204,
  251,
  226,
  168,
  11
]; // WARN: Must generate key first
var cypherCode = <int>[
  i.ci(0, 75),
  i.cp(0, 16),
  i.ci(0, 94),
  i.ci(1, 245),
  i.ci(2, 16),
  i.ci(3, 3),
  i.ci(4, 1),
  i.ci(5, 32),
  i.su(5, 2),
  i.wr(5, 0),
  i.xr(0, 1),
  i.ml(1, 3),
  i.ad(1, 4),
  i.su(2, 4),
  i.jn(2, 6),
  i.ci(0, 31),
  i.ci(1, 0),
  i.ci(5, 32),
  i.ci(6, 16),
  i.rr(2, 0),
  i.rr(3, 1),
  i.xr(2, 3),
  i.wr(5, 2),
  i.su(0, 4),
  i.su(6, 4),
  i.ad(1, 4),
  i.ad(5, 4),
  i.jn(6, 19),
  i.ci(0, 32),
  i.ci(1, 48),
  i.ci(15, 16),
  i.rr(2, 0),
  i.ci(3, 0),
  i.ci(5, 8),
  i.su(5, 4),
  i.ci(6, 0x01),
  i.ci(7, 0x80),
  i.sl(6, 5),
  i.sr(7, 5),
  i.cr(8, 2),
  i.nd(8, 6),
  i.jz(8, 43),
  i.ad(3, 7),
  i.jn(5, 34),
  i.wr(1, 3),
  i.ad(0, 4),
  i.ad(1, 4),
  i.su(15, 4),
  i.jn(15, 31),
  i.ci(0, 0x0F),
  i.ci(1, 0xF0),
  i.ci(5, 16),
  i.ci(6, 64),
  i.wr(6, 0),
  i.ad(0, 1),
  i.xr(1, 0),
  i.su(5, 4),
  i.ad(6, 4),
  i.jn(5, 53),
  i.ci(0, 48),
  i.ci(1, 64),
  i.ci(2, 79),
  i.ci(3, 16),
  i.rr(5, 1),
  i.rr(6, 0),
  i.xr(5, 6),
  i.ad(0, 4),
  i.ad(1, 4),
  i.ad(2, 4),
  i.su(3, 4),
  i.wr(2, 5),
  i.jn(3, 63),
  i.ci(0, 80),
  i.op(0, 16),
  i.st(),
];
