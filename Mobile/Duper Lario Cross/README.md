# Duper Lario Cross

## Category
Mobile

## Estimated difficulty
Medium

## Description
A basic Android app with a hidden crossword that you have to solve.

## Scenario
Lario is trying to save princess Leach from Bowser! Can you help him out? 

## Write-up
The apk can be opened with Jadx-gui. There's only one activity called MainActivity. Inside this activity there's a handler for the button which calls MainActivity.validate().

Inside validate() there is the app gets the input from the textfied (R.id.textField) and passes it to the d() function.

Inside the d() function, a list of strings is generated. The strings are obfuscated:

```java
    private String xjq() {
        return k("onvhq");
    }
    private String k(String str) {
        String methodName = Thread.currentThread().getStackTrace()[3].getMethodName();
        String str2 = "";
        for (int i = 0; i < str.length(); i++) {
            str2 = str2 + ((char) (((((str.charAt(i) - 'a') - (methodName.charAt(i % 3) * 3)) + 2600) % 26) + 97));
        }
        return str2;
    }
```

The k function deduces the name of the calling method (xjq in this case) and uses some vigenere cipher variation to loop over the argument.

After decoding these, the list contains a bunch of popular nintendo related characters.

In the next section we have this:

```java

String lowerCase = "FMGARDIOFIADLEZAGAUHOXHCAEPTSBLBNHONMOWSEWROOCROCPKAIFIAKARROENACERHHRYBRIKNSDKKYISIIKLUHSUWOINHOOUTGELPSDORPIYPOOMOIOIMEBFRLSSENBAAUOWRASHGNILKNISDLY".toLowerCase();
        this.s2 = lowerCase + "";
        Iterator it = arrayList.iterator();
        while (it.hasNext()) {
            String str2 = (String) it.next();
            int i = 0;
            while (i < 15) {
                int i2 = 0;
                while (i2 < 10) {
                    int i3 = i2;
                    int i4 = i;
                    l(lowerCase, str2, i, i2, 1, 0);
                    l(lowerCase, str2, i4, i3, 1, 1);
                    l(lowerCase, str2, i4, i3, 0, 1);
                    l(lowerCase, str2, i4, i3, -1, 1);
                    l(lowerCase, str2, i4, i3, -1, 0);
                    l(lowerCase, str2, i4, i3, -1, -1);
                    l(lowerCase, str2, i4, i3, 0, -1);
                    l(lowerCase, str2, i4, i3, 1, -1);
                    i2 = i3 + 1;
                    i = i4;
                }
                i++;
            }
        }
		```
The code loops over all the words, and loops over the long `lowerCase` string and calls the l function on each position + string, along with different values for 0/1/-1.

The l function looks like this:

```java

    private int l(String str, String str2, int i, int i2, int i3, int i4) {
        int i5 = 0;
        while (i5 < str2.length() && g(str, (i5 * i3) + i, (i5 * i4) + i2) == str2.charAt(i5)) {
            i5++;
        }
        if (i5 == str2.length()) {
            for (int i6 = 0; i6 < str2.length(); i6++) {
                this.s2 = s(this.s2, (i6 * i3) + i, (i6 * i4) + i2);
            }
            return i5;
        }
        return -1;
    }
```

What's going on here, is that the `str` argument is actually a 1D representation of a 2D array. This can be done by mapping each coordinate to (x + y * total_lines). The i and i2 arguments are the position in the grid (x and y), while i3 and i4 are the directo to search in.

The l function searches through the given grid for the given word (str2) and if it finds it, it switches out the found letters in a secondary string (s2). S2 is just a copy of s1 which is copied at the start of the l() function.

By looping over all the words, this will gradually take letters away from s2 until only a few letters are available. Back in d(), we can see that the given password is being validated:

```java
 int i5 = 0;
        for (int i6 = 0; i6 < this.s2.length(); i6++) {
            if (this.s2.charAt(i6) != '-') {
                if (i5 < str.length() && str.charAt(i5) == this.s2.charAt(i6)) {
                    this.s2 = s(this.s2, i6 % 15, (int) Math.floor(i6 / 15));
                }
                i5++;
            }
        }
        return this.s2.replace("-", "").length() == 0;

```
This code searches the remaining letters (s2) and for each letter that is not a dash (-), it checks it against the given password and also replaces those letters in s2. Finally, the function returns true is the entire s2 string consists of the dash character.

The easiest way to solve this is by patching the application to print the value of s2:

```
apktool d lario.apk

```
Add a method to MainActivity.smali:
```smali
.method private d()V
    .locals 2

    const-string v0, "XXX"

    .line 420
    iget-object v1, p0, Lbe/dauntless/duperlariocross/MainActivity;->s2:Ljava/lang/String;

    invoke-static {v0, v1}, Landroid/util/Log;->i(Ljava/lang/String;Ljava/lang/String;)I

    return-void
.end method
```
And call the method before the password is verified. The call is a bit difficult since the k() function has so many local variables.

```
invoke-direct/range {p0 .. p0}, Lbe/dauntless/duperlariocross/MainActivity;->d()V
```

After repackaging the app (`apktool b`) and signing it (e.g. using ubersign), the s2 string will be printed to the logcat:

```
 -m-ar-iofi------g--h-------ts--b--o---wse-r------p--i---ka------c--h----------------------u----h-----elps------poo---------r-----b---ow--------------y
```
By removing all the dashes, we get the password:

```
mariofightsbowserpikachuhelpspoorbowy
```

This password is wrapped by the validate() function to get the flag:

```java
    private void validate() {
        String obj = ((TextInputLayout) findViewById(R.id.textField)).getEditText().getText().toString();
        if (d(obj)) {
            Toast.makeText(this, "CSC{" + obj + "}", 1).show();
        } else {
            Toast.makeText(this, ":(", 1).show();
        }
    }
```


## PoC script
NA

## Flag
CSC{mariofightsbowserpikachuhelpspoorbowy}

## Creator
Jeroen Beckers

## Creator bio
