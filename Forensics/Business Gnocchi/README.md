# Business Gnocchi

## Category
Forensics

## Estimated difficulty
Easy

## Description
Audio is played back through bluetooth headphones. The traffic is sniffed.
The challenge requires students to extract the audio packets.

## Scenario
  We've cornered one of the biggest cryptoterrorists on the planet, and it looks like he knows we're after him.
  He seemed to be listening through his previous phone calls as we approached him, and, we managed to capture his headphones' traffic.
  Can you recover the contents of the call?

## Write-up
The description is fairly straightforward, we need to recover some audio.
We have a pcap that clearly is of bluetooth traffic once it's open, all we have to do is find where the sound could be.

Bluetooth audio happens over `A2DP`, so, searching for it (bta2dp) shows us a continuous stream of sound.
Clicking on it, we can find that it contains `RTP`/Realtime Transport Protocol packets.

Wireshark has a built-in tool to extract such streams in Telephony>RTP>Play the only stream>Click on the source>Export>File Synchronized File.

We need to do this step, as wireshark fails to identify the playback speed. We can play back the exported WAV into any player at 2x speed (with appropriate pitch shifting), and we can hear the flag.

## Solve script
N/A

## Flag
CSC_BIZONACCICOMEBACK

## Creator
Théo Davreux

## Creator bio
I never borght :(
