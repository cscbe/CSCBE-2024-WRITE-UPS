#!/bin/bash
#Create ZSK
dnssec-keygen -a RSASHA256 -b 1024 -3 -K ./ thisistheflag.be
#Create KSK dummy key
dnssec-keygen -a RSASHA256 -b 2048 -3 -K ./ -fk thisistheflag.be

for key in $(ls -1 *.key);do dnssec-dsfromkey $key; done > ./dshashes.txt
