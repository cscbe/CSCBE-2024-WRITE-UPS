# CHALLENGE_TITLE
Yet another ISO...

## Category
Forensic

## Estimated difficulty
Medium

## Description
The concept of the challenge is really simple, it consists of a discussion between two employees of the same company through a VOIP server. To resolve the challenge, you need to use the wireshark tool and retrieve the RTP packets. Wireshark has a feature that allow to retrieve the VOIP call and you can play the stream. During the call, the two employees are talking about a ZIP file, and one of them said that he's actually downloading it. 
You can retrieve the HTTP stream and download the ZIP file. The password of the archive is given in the discussion.
The flag is located in the archive. 

## Scenario
The CEO of the company "Societerre" Andrew, harbors suspicions regarding the productivity of two employees, Sam and Jacob, suspecting that they might be slacking off and neglecting their important duties. 

In response, Andrew asked the IT team to monitor their network traffic. As the forensic investigator for the company, you have been tasked to analyze the captured network data to uncover any evidence that might support Andrew's suspicions.

(This challenge was made with assistance from Antoine T.)
## Write-up
1. Open the captured traffic on Wireshark and identify a HTTP traffic downloading a ZIP file and RTP packets (VOIP)
2. On the high tabs, click on Telephony --> VOIP calls
3. Take the second call between Jacob and Sam. 
4. Export with the "Stream Syncronized audio"
5. Listen the call. At the end of the call, they give the password of the zip archive
6. Take the HTTP stream, download the archive and use the password to decrypt it. 
7. Enjoy the flag!

## Solve script

## Flag
CSC{3ncrypt_Y0ur_V0!P}

## Creator
Yannis Kireche & Antoine T. 

## Creator bio
Yannis Kireche : CTF enthusiast & currently working @ Thales as a network and cloud security consultant.
Linkedin: https://www.linkedin.com/in/yanniskireche/

Antoine T. : Cyber Threat Intel analyst.