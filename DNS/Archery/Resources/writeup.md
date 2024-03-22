# CSCBE 2024 - Challenge: Archery

# Introduction

```
Once upon a time, in a far-off land of technology and wonder, the skilled hackers known as 
the Knights of the Binary Table safeguarded the kingdom's cyber infrastructure, protecting its secrets. 
Chaos ensued when the evil sorcerer Maliciousus corrupted the kingdom's DNS records, plunging it into darkness. 
Tasked with restoring the DNS records, the Knights of the Binary Table embarked on a quest to decipher 
Maliciousus's spell and uncover the crucial timestamp hidden within.
The domain of this kingdom was <code>knightsofthebinarytable.be</code>
```


## Solution 

1. 
```
dig knightsofthebinarytable.be 
;; ANSWER SECTION:
knightsofthebinarytable.be. 3600 IN	A	0.0.33.44

;; AUTHORITY SECTION:
knightsofthebinarytable.be. 86400 IN	NS	ns1.knightsofthebinarytable.be.
knightsofthebinarytable.be. 86400 IN	NS	ns2.knightsofthebinarytable.be.

;; ADDITIONAL SECTION:
ns1.knightsofthebinarytable.be.	1368 IN	A	3.250.27.124
ns2.knightsofthebinarytable.be.	1562 IN	A	34.242.152.175

```

That's a weird IPv4 address. Let's query that again.

2. 
```
dig knightsofthebinarytable.be -t A
knightsofthebinarytable.be. 3549 IN	A	0.0.32.93
```

Querying the server shows an IPv4 value in the A record with a decreasing timer (counting down to the next minute on which the flag will be shown). However, the TTL has been set to a value that is way too large, meaning that cached values in resolvers will most likely not contain the flag.

3. 
```
dig knightsofthebinarytable.be @ns1.knightsofthebinarytable.be -t any
knightsofthebinarytable.be. 3600 IN	A	0.0.31.2
knightsofthebinarytable.be. 86400 IN	NS	ns1.knightsofthebinarytable.be.
knightsofthebinarytable.be. 86400 IN	NS	ns2.knightsofthebinarytable.be.
knightsofthebinarytable.be. 3600 IN	TXT	"Check again in this IPv4 amount of time and we'll give you the flag."
knightsofthebinarytable.be. 3600 IN	TXT	"We're sorry it Takes This Long"
```

4. 
```
dig knightsofthebinarytable.be @ns1.knightsofthebinarytable.be -t A
knightsofthebinarytable.be. 3600 IN	A	0.0.30.30
```

To solve this, you have to query directly to the authoritative server on the timestamps that it is counting towards.

Example: `watch -n 1 dig knightsofthebinarytable.be @ns1.knightsofthebinarytable.be -t any`


# How to run

This challenge assumes:
- that the domain knightsofthebinarytable.be is registered
- its authorative nameservers are pointing to a server running the provided python script
- the nameserver's IPs are entered in the script.
- The timestamps in the script are changed to the deployment period. If you're using this challenge for something else than the Cybersecurity Challenge Belgium qualifiers of 2024, change the timestamps in main.py to include some timestamps in your challenge's timespan.

Deployment can be done using the **Dockerfile** (`docker build -t binarytable && docker run -p 53:53/udp binarytable`) or with the following commands.

```
python -m venv .venv
source .venv/bin/activate
python main.py
```

The IP of the nameservers should not be given to the participants (they should be able to deduct them from the dns lookups).

The challenge is stateless, meaning that it can be scaled in case of a DDoS.
