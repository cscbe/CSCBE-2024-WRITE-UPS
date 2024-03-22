# Flag Communicator

## Category
Mobile

## Estimated difficulty
Medium

## Description
A flutter app sends a request to the server to download a flag.
The app has a self-signed certificate pinned, to prevent interception.
Use [this writeup by Jeroen Beckers to solve it](https://blog.nviso.eu/2022/08/18/intercept-flutter-traffic-on-ios-and-android-http-https-dio-pinning/)

## Scenario
  We caught a wild technomancer, he won't be able to terrorize little programs anymore!
  We have a few of his nasties left to deal with, he seemingly used this one to get his flags delivered straight to him.
  The app is rebelling, and refuses to give us the flag by eating it as soon as it gets it.
  Can you grab it before it gets engulfed in it's greedy maw?

## Write-up
The received app is easy to pin as being made with flutter:
- The icon is the default flutter icon
- The splash screen looks like flutter's
- There is a libflutter.so file in the apk

When the app opens, we are prompted to press the button to download the flag.
It works, it said it worked, but that's it.

When we intercept the flag, using something like HTTP Toolkit, we can see exception details.
In said details, we can see that DIO complains that the certificate is incorrect.
If we talk to the server ourselves, we can see that it speaks HTTPS, and that it seems to always return HTTP 400.

Combining a search of "Flutter, Dio, HTTPS" and some keywords like "bypass", we eventually get onto this writeup:
https://blog.nviso.eu/2022/08/18/intercept-flutter-traffic-on-ios-and-android-http-https-dio-pinning/

Now, if you have a rooted emulator, it will pretty much work as-is.

I used Frida-Gadget to patch the APK
`frida-gadget flag_communicator.apk --arch x86_64`

Then I re-signed it using apk-signer
`apk-signer flag_communicator.apk`

Installed it via adb
`adb install flag_communicator_signed.apk`

Downloaded the script referred to in the writeup
`wget https://raw.githubusercontent.com/NVISOsecurity/disable-flutter-tls-verification/main/disable-flutter-tls.js`

Started the app, and connected to a frida-gadget session:
`frida -U -l .\disable-flutter-tls.js --pause Gadget`

Installed [HTTP Toolkit](https://httptoolkit.com/), both the desktop and android versions
Selected "connect via ADB"
And clicked the button, you can see the flag in the interceptor's window.

If your reverse proxy isn't cooperating, but you can grab the bytes of the request on it's way out, you can also perform the request yourself.

## Solve script
N/A

## Flag
CSC{b1g_5n4CC_foR_th4_3VI1_ST4cc!}

## Creator
Théo Davreux

## Creator bio
Too dangerous with a computer, I'm just sharing the load of the suffering I cause. Sorry.