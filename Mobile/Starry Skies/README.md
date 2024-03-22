# Starry Skies

## Category
Mobile

## Estimated difficulty
Hard

## Description
A flutter app in profile mode is given to the students.
Start the app with extra boolean values that are used to start the app's debug port when using `flutter run`
Once done, attach to the VM service (either manually, through `flutter attach`, or via vscode's attach command), start devtools, and inspect the memory to find the main widget, containing `myPocket`, which has the downloaded flag.

## Scenario
  We've barely caught the technomancer, and he's already escaped!
  We're already planning on raiding his Observatory again, but we need a flag to get in.

  It seems that he's doubled down on his app's security, but he seemingly ignored performance in the meantime, what a stuttery mess!
  We've done all of our negociation techniques, but the program refuses to cooperate once again!
  Can you pick the pocket of this evil program, and give us the key to the technomancer's Observatory?

## Write-up
We receive the app named `app-profile.apk`, we can also quickly determine the app is flutter as with the previous challenge in the series:
- Flutter logo
- Flutter splash screen
- libflutter.so in the apk

Now, the app isn't in debug mode, so we can't just extract the source, but it's not in release mode either, there are tools left in it.

There is a hint to the word "Observatory" in the description of the challenge, searching for it, we can find multiple pages about debugging flutter, and specifically references to profile mode.

Trying to access the observatory normally *will not work*, as it does not pass the additional arguments required to listen to the observatory port.
But, when running an app with `flutter run --profile`, the observatory opens. If we do `flutter run --profile -v`, we can see that the very last command it executes is:
`adb.exe -s emulator-5554 shell am start -a android.intent.action.RUN -f 0x20000000 --ez enable-dart-profiling true --ez enable-checked-mode true --ez verify-entry-points true space.railgun.flag_communicator/space.railgun.flag_communicator.MainActivity;`

(With differences relating to package name)

If we copy/paste this command into a terminal, even if we aren't actively running a debug session, the app will open, and it will listen for connections, we can see this via `adb logcat`:

`02-26 18:03:15.610  6306  6348 I flutter : The Dart VM service is listening on http://127.0.0.1:40895/bL8hwfbfhNs=`

Once this is visible, either forwarding the port manually (via `adb forward`), attaching then accessing ((via `flutter attach`), or using an IDE like VS Code to attach (`>Debug: Attach to Flutter on Device`) will make the port available, then, we can use devtools (either launching it manually, or, via vs code, `Dart: Open DevTools Memory Page`) will let us browse the currently active Objects.

We can see two peculiarly named objects: `TheCatThatHoldsTheFlag` and `_TheCatThatHoldsTheFlagState`, if we click over the `1` in the `Instance` column, a menu lets us inspect the object in the console, revealing the flag to us in the variable `myPocket`.

Alternatively, you can go to the network tab, and intercept the network request, if you manage to do so.

## Solve script
N/A

## Flag
CSC{pr0f1l3_Th1S_You_fi11hy_c45UA7}

## Creator
Théo Davreux

## Creator bio
wololo
