# Bad Ransomware

## Category
Forensics

## Estimated difficulty
Extreme

## Description
Ransomware encrypted file by "connemara" with a slight variation on the magic sequence.

## Scenario
  A cookie factory was attacked by the “Bad Ransomware!” ransomware gang.
  All their cookie recipes have been encrypted.
  It is your job to recover the cookie recipes!
  You have one advantage: you know that the cryptographic design of their ransomware application is flawed.
  Good luck!

## Write-up
This ransomware (a real sample) partially encrypts the ransomed files (for performance reasons). Each file is divided in 10 blocks, and that start of each block is encrypted, not the rest.

The metadata added by the ransomware application (after magic sequence RANSOMWARE_METADATA) defines which part of the file have been encrypted: POSITION1:SIZE#POSITION2:SIZE#...

Encryption is done with XOR using a 16-byte long key: the first 16 bytes of a block are encrypted with that key, then the next 16 bytes of that same block are encrypted with the same key, and so on, until the first 256 bytes of each block are encrypted.

The encrypted file is a ZIP file. ZIP files contain redundant information: each file stored inside a ZIP container has 2 records: a ZIPFILE record and a ZIPDIRRECORD. Each type of record contains information like the filename, file timestamps, ... A ZIP file is build up of a series of ZIPFILE records, each followed by the compressed file content. There is one ZIPFILE record per file. After all ZIPFILE records plus compressed data have been stored inside the ZIPFILE, the ZIPDIR records are appended. There is also one ZIPDIR record per file. And finally, a END OF DIRECTORY record is appended.

Because the ransomed file is partially encrypted, the first ZIPFILE record is encrypted, but the corresponding ZIPDIR record is not. With the redundant information in the ZIPDIR record, the first 16 bytes of the ZIPFILE record can be reconstructed, and thus the 16-byt XOR key can be recovered (by XORing the ciphertext with the cleantext).

NVISO has handled a case with ransomware just like this. The only thing that was changed in the metadata, is the magic sequence: this was not RANSOMWARE_METADATA.

## Solve script
```sh
connemara-extract-keystream.py -z -w keystream.bin cookies.zip.Encrypted

connemara-decryptor.py -k keystream.bin cookies.zip.Encrypted
```

## Flag
CSC{HD6E8HDKZNDKE090AJ}

## Creator
Didier Stevens

## Creator bio
Didier Stevens (Microsoft MVP, SANS ISC Handler, Wireshark Certified Network Analyst, …) is a Senior Analyst working at NVISO. Didier is a pioneer in malicious PDF document research and malicious MS Office documents analysis and has developed several tools to help with the analysis of malicious documents like PDF and MS Office files. Didier regularly participates in pentests and red team engagements to create task-specific documents. You can find his open source security tools on his IT security related blog
