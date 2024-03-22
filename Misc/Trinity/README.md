# Trinity

## Category
Misc

## Estimated difficulty
Hard

## Description
This challenge features a relatively straightforward form of audio steganography by hiding a text message in the spectrogram of a sound fragment. In this case, the message contains the flag, encrypted with a Vigenère cipher. The key to solve the cipher is hinted within the same message.

Theme: Barbenheimer

## Scenario
Operative, we need your help. One of our field agents has been made and fled the safehouse before we could safely extract them from enemy territory. Currently, we have no idea where they could've gone, but we are fearing the worst. To make matters worse, we were expecting a vital communication from them containing the password to open a file with nuclear launch codes. If we cannot retrieve this message, well... Strictly speaking, you don't have the needed security clearance to know what would happen *exactly*, but you're a smart cookie. I'm sure you can put two and two together. It starts with the letter "A" and rhymes with "Barmageddon".

We have one last hope, however. Our black ops team has retrieved the laptop our field agent was using and was still hidden in the safehouse, from which they could recover a single video file. Perhaps it contains the message we so desperately need?

## Write-up
1. Open the provided 'oppie.mp4' file in an audio editing application, such as Audacity.
2. By swapping the view from "Waveform" to "Spectrogram", a hidden message is revealed, stating "Tell me, Vig. AmIKenough? CEK{KWGF4HMLG4YMDLRCHRFWUVXMAUGUCE1EVYXGCJR4F}".
3. A first glance at the hidden message shows a part that looks suspiciously similar to a flag! But it still seems to be tampered with somehow, because it doesn't start with 'CSC'.
4. The way to decode the flag is hinted at in the first part of the message. Indeed, the flag is encrypted with a Vigenère cipher, with the key 'AmIKenough'. Once you know this, decryption is trivial.
5. Decrypting the Vigenère cipher with the appropriate key (e.g. using a tool like CyberChef) yields the flag: CSC{ASTR4NGEG4METHEONLYWINNINGMOVE1SNOTTOPL4Y}.

## Solve script
Not Applicable. Challenge does not involve any running processes or components.

## Flag
CSC{ASTR4NGEG4METHEONLYWINNINGMOVE1SNOTTOPL4Y}

## Creator
Jonah Bellemans

## Creator bio
Jonah is a doctoral researcher at KU Leuven’s DistriNet Research Group. His research focuses on Privacy Engineering in the early stages of software architecture and development. Previously, he obtained his Master's degree in Computer Science in 2020 and wrote a thesis on the security and privacy of Smart Home IoT Devices.
 
Additionally, he has obtained an Advanced Master's degree in ICT & Intellectual Property Law (LL.M) at KU Leuven's Centre for IT & IP Law (CiTiP) in 2022, where he wrote a thesis on the compatibility of the existing EU privacy & data protection regulation with the EU regulatory framework for Anti-Money Laundering and Countering the Financing of Terrorism (AML/CFT). From 2019 until 2023, he worked as a consultant in the private sector, with a particular focus on Governance, Risk & Compliance in cyber security.
 
His primary interests are privacy & data protection, ICT law, software architecture, threat modeling, and security incident & crisis management.

- https://www.linkedin.com/in/jonahbellemans/
- https://distrinet.cs.kuleuven.be/people/JonahBellemans/
