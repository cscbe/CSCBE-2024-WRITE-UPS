# Locked

## Category
Mobile

## Estimated difficulty
Easy

## Description
Easy decompilation of Android apk

## Scenario
The app is locked. Can you get in?

## Write-up
Open the application in an Android decompiler, for example JADX-GUI.

The MainActivity looks like this:

```java
public class MainActivity extends AppCompatActivity {
    /* JADX INFO: Access modifiers changed from: protected */
    @Override // androidx.fragment.app.FragmentActivity, androidx.activity.ComponentActivity, androidx.core.app.ComponentActivity, android.app.Activity
    public void onCreate(Bundle bundle) {
        super.onCreate(bundle);
        setContentView(C0567R.layout.activity_main);
        init();
    }

    private void init() {
        ((Button) findViewById(C0567R.C0570id.submitButton)).setOnClickListener(new View.OnClickListener() { // from class: be.dauntless.lock.MainActivity.1
            @Override // android.view.View.OnClickListener
            public void onClick(View view) {
                EditText editText = (EditText) MainActivity.this.findViewById(C0567R.C0570id.inputText);
                Toast.makeText(MainActivity.this, editText.getText().toString().equals(MainActivity.this.getResources().getString(C0567R.string.app_version)) ? MainActivity.this.getResources().getStringArray(C0567R.array.flags)[editText.getText().toString().length() * 7] : "Wrong flag :(", 1).show();
            }
        });
    }
}
```
The code waits for the user to click the button and then retrieves the content of the only inputText in the layout. It compares the given value to R.string.app_version which can be found in the resources folder:

```xml
 <string name="abc_shareactionprovider_share_with_application">Share with %s</string>
    <string name="abc_toolbar_collapse_description">Collapse</string>
    <string name="androidx_startup">androidx.startup</string>
    <string name="app_name">Locked</string>
    <string name="app_version">0p3nS3s4m3</string>
    <string name="appbar_scrolling_view_behavior">com.google.android.material.appbar.AppBarLayout$ScrollingViewBehavior</string>
    <string name="bottom_sheet_behavior">com.google.android.material.bottomsheet.BottomSheetBehavior</string>
```
So the password is `0p3nS3s4m3`. We can now run the app dynamically to get the flag, or we can follow the logic. The length of the string (=10) is multiplied by 7 and that string is taken from res/values/arrays.xml:

`CSC{2473da7a332d33a596cf380a3734409a}`

## Solve script
NA

## Flag
CSC{2473da7a332d33a596cf380a3734409a}

## Creator
Jeroen Beckers

## Creator bio
See others
