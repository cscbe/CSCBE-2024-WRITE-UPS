# Weaponized Private Army

## Category
Forensics

## Estimated difficulty
Easy

## Description
PCAP of a wpa handshake, can be cracked quickly with rockyou.
Recover the flag in an http packet you can read by giving the password to wireshark.

## Scenario
  Mr Prime Minister!
  We've intercepted the communications of a dangerous PMC owner, one of our agents was on his flight, and he appeared to access secret plans for his "Inner Hell" offshore military base.
  Everyone here at the agency has tried to decrypt what our agent recovered, but none have managed to recover the secret plans...

  We've heard you have 1337 H4XX0R 5K1LL5, you have to help us, like a true Patriot!

## Write-up
The received pcap contains, most notably, 802.11 frames.

It appears to contains multiple probe response and authentication frames.

Since this appears to be a capture of nothing but WiFi frames, the first step would be to crack it.

`aircrack-ng challenge.cap -w rockyou.txt`

Gives us the password, `goodlife`

We can also find the password as the default password of the `GL-AR750` wifi router on google.

Once we have the password, we can give it to Wireshark in Edit>Preferences>Protocols>IEEE 802.11>Decryption Keys, then add a key in the format `wpa-pwd` with the password `goodlife`

Frames are now decoded in Wireshark, we can then find an HTTP request for `flag.txt`, containing our flag.

## Solve script
N/A

## Flag
CSC{protected_access_unless_you_got_ears}

## Creator
Théo Davreux

## Creator bio
Definitely not part of the La Li Lu Le Lo