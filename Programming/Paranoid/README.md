# Paranoid

## Category
Programming

## Estimated difficulty
Hard

## Description
A flawed string compare algorithm that allows for timing attacks. Both a password and a OTP need to be guessed. The OTP cannot be brute-forced, since only limited tries are available before the OTP is changed. The response of the server includes the result of <string.h strcmp()>, allowing for logarithmic search and guessing the OTP within limited tries.

## Scenario
I made this cool website, but I don't trust any of those lousy package maintainers to handle my password securily. So, I developed my own library. I know it's security because it uses MFA.

## Write-up
When entering a random password, a request is made to a backend server. In the response of this request, we can see that the password is wrong.
However, other information is provided as well: how long it took the server to validate the correctness of the password, and a "result" code.

From this point, we use Python for making requests to the backend server to automate things.

After trying a few more random passwords, we can find that the "result" code can be either "1" or "-1", but it does seem to be consistent for a given input. Since there is limited other info to examine, we continue with this field. We try to find the meaning of this "result" code, by trying to find the way this is calculated.

After trying all (readable) single ASCII characters, we find that we can group all characters <= M give the result 1, and all other give result -1. We also notice a clear bump in execution time. So, is a timing attack possible? 

A brute-force algorithm can use the bump in execution time to detect when a character is correct and try to find the next. This way we don't need to try ALL possible combinations, significantly increasing our speed (and load on the server).

When we find the correct password and submit it to the server, we get a different response, but not a flag. We try this password out in the browser.
There we find that a 2FA code (OTP) is required as well. We try our same 'smart' brute force algorithm, but this doesn't work. There are only limited attempts at guessing the 2FA code, and our brute force algorithm needs many more.

We still haven't really used the 'result' property of the response JSON. Much like when guessing the password, the value of 'result' changes depending on the provided 2FA code. It splits the possible input characters into 2 distinct groups:


)
````
(simplified example using 'result' when guessing the first character of the password) 

1 : [A, B, C, D, E, F, G, H, I, J, K, L, M]
-1: [N, O, P, Q, R, S, T, U, V, W, X, Y, Z]
````

What do we know when guessing the first character of the real password when trying elements of the first group? The actual character we are looking for is 'greater'. For 'M', the correct character, we can combine our knowledge that the password is validated character per character and that the next character is 'o'. This is also greater than 'M' in ASCII.

A similar reasoning for the second group applies.

We have now found the meaning of the 'result' field in the response JSON.  It has the same properties of the `string.h strcmp()` function.

But how can this help us?
Since we know if we need to 'higher' or 'lower' for the currect character we are guessing, a full brute force of all single ASCII characters is no longer necessary. Instead, we can narrow it down to the subset of ASCII characters that are either smaller or larger than the current character.
In essence halving our search space with each guess.

==> In logarithmic time, we can find the next character. So instead of the previous brute-force attack combined with a timing attack, we can now implement the timing attack with a binary search algorithm. This is fast enough to guess the OTP without it resetting.

## Solve script
PUT IT IN THE `Resources` FOLDER AND MENTION IT IN THE `healthcheck:` of `challenge.yml`

## Flag
CSC{Al9ORi7hMic5_cLa22_Wa5_Co0L_aF73R_AlL}

## Creator
Arno Vermote

## Creator bio
Arno is a 2022 and 2023 CSCBE finalist and all-round tech nerd. He currently works as a Security Engineer at Bank J. Van Breda & C°, with a focus on security operations and monitoring. When not behind his desk, he enjoys going for a ride on his motorcycle.  
