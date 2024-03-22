# Puzzle - “thisistheflag scavenger hunt”

## Start puzzle

`docker-compose down && docker-compose build --no-cache && docker-compose up -d; docker-compose logs -f`

This will start an authoritative DNS server for domain: thisistheflag.be\
`$ dig @127.0.0.1 thisistheflag.be soa +short`\
`ns1.thisistheflag.be. what.about.txt. 17 3600 1800 2419200 600`

## Verify puzzle is ready and setup

```
dig @127.0.0.1 901C3E6681DFC7F1090977E9D2C15CADD69D5B80.thisistheflag.be. -t txt +short
"CSC{xn--80agbesolha6bhblgn}"
```

## Introduction


```
Humpty Dumpty built an tunnel so fine, securing his connections, line by line. 
But with one mistake, he took a great fall, And **<ip goes here>** couldn't protect him at all.
All the king's cryptographers and all the king's geeks, Tried to find the lost secret, despite the leaks. 
But with thisistheflagdotbe denied and data adrift, Poor Humpty remained in a security rift.

```

## Solution (including hints)

1. 
```
dig @127.0.0.1 thisistheflag.be. -t any | grep SRV
thisistheflag.be.	86400	IN	SRV	10 60 22 ssh.thisistheflag.be.
thisistheflag.be.	86400	IN	RRSIG	SRV 8 2 86400 20510710122239 20240223135644 10378 thisistheflag.be. mZu1Sdbn2Rft8DaP07xPFBzHDaZGHNowEX6R4ulzYZf5dHjdlkuOatrC Z7uFvxpHaAcm3c5M+Xq6QhdHvlLaRbeC4eSOwnxKUTe8A/EfQcXDVAMx 67HRc47RaNrSNBDIhuCqmb2J/llx075KZZfJC3aYap6nLRtRaDMcomMm r2s=
```

SOA record shows a hint  : what.about.srv.


2.
```
ssh whatever@127.0.0.1 -p 22
The authenticity of host '127.0.0.1 (127.0.0.1)' can't be established.
ED25519 key fingerprint is SHA256:kSxrS/mL/BAx2jkwHW3bE9hGza2UWZ0TZaluMLK2nJM.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '127.0.0.1' (ED25519) to the list of known hosts.
Look further ECDSA sha-1 contains the flag
Look further ECDSA sha-1 contains the flag
Look further ECDSA sha-1 contains the flag
Look further ECDSA sha-1 contains the flag
Look further ECDSA sha-1 contains the flag
Look further ECDSA sha-1 contains the flagwhatever@127.0.0.1: Permission denied (publickey,gssapi-keyex,gssapi-with-mic).
```

3.
```
 dig @127.0.0.1 ssh.thisistheflag.be. -t sshfp +short
3 1 901C3E6681DFC7F1090977E9D2C15CADD69D5B80
4 1 327692C38CAAE3A0FFC29869CB0BEA522B60ED23
3 2 68B8813AFFA2CEE1D727C3C9E92A6EE63FD3A7330C99E4A7BB869D4E CABD6B8C
1 1 3704F069D4E54D93D72156085942E5C327731EAA
4 2 82D76FDB632A122F12B3DFFA0BBD2715727F44AFF86568E3FD3F1D4E EAB2DE70
1 2 065C885BAF91069D6B291D453A08318B1D2A31415C5AF2D3C6FA8532 4FE1E5F9
```



4. 
Let's do a query on ECDSA sha-1 as actual subdomain
```
dig @127.0.0.1 901C3E6681DFC7F1090977E9D2C15CADD69D5B80.thisistheflag.be. -t txt +short
"CSC{xn--80agbesolha6bhblgn}"
```


## Troubleshoot

To troubleshoot individual running containers
 Example: docker exec -it thisistheflag_be_authoritative /bin/bash


rebuild one service
Example:
 docker-compose rm -sv thisistheflag_be_authoritative; docker-compose up -d --build; 
 docker-compose rm -sv thisistheflag_be_authoritative; docker-compose up --build -d thisistheflag_be_authoritative
