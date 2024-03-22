# Puzzle - “thisistheflag treasure hunt”

## Start puzzle

`docker-compose down && docker-compose build --no-cache && docker-compose up -d; docker-compose logs -f`

This will start an authoritative DNS server for domain: thisistheflag.be\
`$ dig @127.0.0.1 thisistheflag.be soa +short`\
`ns1.thisistheflag.be. what.about.txt. 17 3600 1800 2419200 600`

## Verify puzzle is ready and setup

`$ dig @localhost thisistheflag.be -t txt +short`\
`"CSC{youfoundtheflag}"`

## Introduction


```
iemie, mienie, minie, moe,
Pienie, puny, mighty joe
Where is my flag, friend or foe?
⟩⟩⟧⟥⟡⟦⟐⟜⟩⟧⟙.be
Maybe "insert ip adress" has the answer, no?
```

## Solution (including hints)

1. `⟩⟩⟧⟥⟡⟦⟐⟜⟩⟧⟙.be` translate to `xn--thisistheflag.be` ( puny code )

**HINT1**: puny code

2.  Let's query `dig @localhost thisistheflag.be -t  any`\
`$ dig @localhost thisistheflag.be -t any +short`\
`ns1.thisistheflag.be. what.about.txt. 17 3600 1800 2419200 600`

SOA record shows a hint  : what.about.txt.

**HINT2**: TXT record

3. Let's query TXT record thisistheflag.be -t txt +short 
Result: "CSC{youfoundtheflag}"


## Intended weird ANY behaviour in puzzle explanation
The weird behaviour when DNS querying for an ANY record is intended in this puzzle.\
This DNS server (running NSD) is not answering with all records (as would be expected), but answers with only 1 RRset (RFC8482)


## Troubleshoot

To troubleshoot individual running containers
 Example: docker exec -it thisistheflag_be_authoritative /bin/bash


rebuild one service
Example:
 docker-compose rm -sv validating_resolver; docker-compose up -d --build; 
 docker-compose rm -sv thisistheflag_be_authoritative; docker-compose up --build -d thisistheflag_be_authoritative







