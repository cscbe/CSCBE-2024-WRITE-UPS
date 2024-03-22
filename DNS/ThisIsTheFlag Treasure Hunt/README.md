# ThisIsTheFlag Treasure Hunt

## Category
DNS

## Estimated difficulty
Medium

## Description
This text mentions the quick technical details about the challenges. It is only used by the CSCBE internal CTF team.

## Scenario
iemie, mienie, minie, moe,
Pienie, puny, mighty joe
Where is my flag, friend or foe?
⟩⟩⟧⟥⟡⟦⟐⟜⟩⟧⟙.be
Maybe "insert ip adress" has the answer, no?

*note: modified "insert ip adress" with "the server below"*

## Write-up
1. `⟩⟩⟧⟥⟡⟦⟐⟜⟩⟧⟙.be` translate to `xn--thisistheflag.be` ( puny code )

**HINT1**: puny code

2.  Let's query `dig @localhost thisistheflag.be -t  any`\
`$ dig @localhost thisistheflag.be -t any +short`\
`ns1.thisistheflag.be. what.about.txt. 17 3600 1800 2419200 600`

SOA record shows a hint  : what.about.txt.

**HINT2**: TXT record

3. Let's query TXT record thisistheflag.be -t txt +short 
Result: "CSC{youfoundtheflag}"

## Solve script
Not Provided

## Flag
CSC{youfoundtheflag}

## Creator
DNS Belgium

## Creator bio
