                                                                                     **
# Grandpa Hubert's grandson

## Category
Cryptography

## Estimated difficulty
Medium

## Description
Simple hash cracking using custom wordlist based on the challenge description

## Scenario
Hey everyone!

My grandson, Alex Robinson, asked me to write a small text for you all since you seem to enjoy our challenges. Did you know that Alex was born in the 2000s? He is still young but has already found a job. He is currently living in Anderlecht, which is quite annoying for me as it is far from my place. He doesn't come to visit me at home that often, but I'm okay with that as I have "Blopblop," my goldfish. Additionally, I sometimes go see Alex at his badminton club where his friends like to call him "Robyeye" because he always say yes for a game of badminton.

I hope you learned a bit more about me!

Regards,
Grandpa Hubert

## Write-up
Looking at the most important key words, we can make the following list:
Alex, Robison, 2000, Anderlecht, Goldfish, Blopblop, Badminton, Robyeye

Using that list in combinaison with cupp, we can create a persona password:
```
  
➜ cupp -i
 ___________ 
   cupp.py!                 # Common
      \                     # User
       \   ,__,             # Passwords
        \  (oo)____         # Profiler
           (__)    )\   
              ||--|| *      [ Muris Kurgas | j0rgan@remote-exploit.org ]
                            [ Mebus | https://github.com/Mebus/]


[+] Insert the information about the victim to make a dictionary
[+] If you don't know all the info, just hit enter when asked! ;)

> First Name: Alex
> Surname: Robinson
> Nickname: Robyeye
> Birthdate (DDMMYYYY): 2000

[-] You must enter 8 digits for birthday!
> Birthdate (DDMMYYYY): 00002000


> Partners) name: 
> Partners) nickname: 
> Partners) birthdate (DDMMYYYY): 


> Child's name: 
> Child's nickname: 
> Child's birthdate (DDMMYYYY): 


> Pet's name: Blopblop
> Company name: 


> Do you want to add some key words about the victim? Y/[N]: Y
> Please enter the words, separated by comma. [i.e. hacker,juice,black], spaces will be removed: Badminton
> Do you want to add special chars at the end of words? Y/[N]: N
> Do you want to add some random numbers at the end of words? Y/[N]:N
> Leet mode? (i.e. leet = 1337) Y/[N]: N

[+] Now making a dictionary...
[+] Sorting list and removing duplicates...
[+] Saving dictionary to alex.txt, counting 336 words.
[+] Now load your pistolero with alex.txt and shoot! Good luck!
```

And now use that wordlist to bruteforce the password:
```
~  
➜ john hash.txt --wordlist=alex.txt 
Using default input encoding: UTF-8
Loaded 1 password hash (sha256crypt, crypt(3) $5$ [SHA256 128/128 ASIMD 4x])
Cost 1 (iteration count) is 5000 for all loaded hashes
Will run 6 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
robyeye2000      (?)
1g 0:00:00:00 DONE (2024-02-29 07:37) 16.66g/s 5600p/s 5600c/s 5600C/s 000000..xela_2020
Use the "--show" option to display all of the cracked passwords reliably
Session completed
~  
➜ john hash.txt --show                    
?:robyeye2000

1 password hash cracked, 0 left
~  
➜ 
```


## Solve script
PUT IT IN THE `Resources` FOLDER AND MENTION IT IN THE `healthcheck:` of `challenge.yml`

## Flag
robyeye2000

## Creator
Julian Dotreppe

## Creator bio

