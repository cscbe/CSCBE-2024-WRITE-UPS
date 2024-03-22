# Quantum Eye

## Category
Web

## Estimated difficulty
Medium

## Description
In this challenge, students must access an admin page that is normally only accessible from localhost using a screenshot tool. The admin page contains a button that leads to the flag. The issue is that the students cannot see where the button leads, and must therefore try and access the HTML source of the admin page.

## Scenario
ShadowNet wields the QuantumEye, a cutting-edge surveillance tool capturing snapshots of encrypted web pages. Your challenge involves navigating through the net underworld, breaching ShadowNet' formidable defenses and hacking the QuantumEye system. 

## Write-up
The players are presented with a screenshot tool that allows them to take screenshots of the CSCBE website and localhost. The must then access the admin page through the tool where they can see a button named flag. The players must then access the source code of the page to see what the button does, which they can do by prepending `view-source:` to the URL. Now that the players have the location of the flag, they can retrieve it through the screenshot tool once again.

## Solve script
N/A

## Flag
CSC{S0MEoN3_is_Alw4y5_waTch1N9}

## Creator
Julien Pepinster & Yannis Kireche

## Creator bio

### Julien Pepinster
Penetration tester at NTT, I always loved breaking stuff and now I get to do it for a living. The CSCBE was one of the reason I started playing CTFs, focused my attention to offensive security and found my passion. I am now returning the favor with some challenges, hoping you all have fun, and some headaches too.
- https://www.linkedin.com/in/julienpeps/

### Yannis Kireche
CTF enthusiast & currently working @ Thales Cyber Solutions as a network and cloud security consultant. 
- https://www.linkedin.com/in/yanniskireche/
