# Get rich fast

## Category
Forensic

## Estimated difficulty
Medium

## Description
The challenge revolves around the concept of exploiting a CVE known as aCropalypse (https://en.wikipedia.org/wiki/ACropalypse), which involves vulnerability in Microsoft Snipping Tool. The goal is to retrieve the original image from a cropped image.
You can do that by using a tool (here is a PoC of how exploit this vulnerability : (https://github.com/frankthetank-music/Acropalypse-Multi-Tool/))

## Scenario
I remember that Julian told me about a secret way to get rich few months ago. However, I've completely wipe my phone since then and only recovered this cropped screenshot from my computer. Could you help me so that we can both get rich ?

## Write-up
First thing to do is to exfiltrate all the exif metadata using exiftool. You'll understand that the screenshot has been cropped by using the Windows Snipping Tool. 
Once you have identified that this image is potentially impacted by the aCropalypse vulnerability. Use one of the different POC scripts thay you can find on Github and select the screenshot (by example: https://github.com/frankthetank-music/Acropalypse-Multi-Tool/). 
You need to provide the original resolution of the image. You can easily guess it because you have the width and you know that the screenshot comes from an iPhone.
Screen resolution of the original image : 1170 x 2532

## Flag
CSC{buck3l_up_n_b4nk_!t}

## Creator
Yannis Kireche

## Creator bio
CTF enthusiast & currently working @ Thales Cyber Solutions as a network and cloud security consultant.
Linkedin: https://www.linkedin.com/in/yanniskireche/