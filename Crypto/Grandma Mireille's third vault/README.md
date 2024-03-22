# Grandma Mireille's Third vault

## Category
Cryptography

## Estimated difficulty
Extreme

## Description
The challengers will recieve an example, an excel sheet of historical weather data and a txt file with altered weather data.
The students first have to analyse the example and try to figure out the encryption method.
Then they have to look at the txt file and notice what data has been changed (some lines are unaltered and thus noise)
Step by step they then have to solve challenge by finding the ASCII value of each line of altered weather data.


## Scenario
  Besides reading books, she also loved to look at the weather.
  She even kept records of weather in Brussels since 1945 !
  But, when I was looking at the data she noted down from 1970, there seemd to be some strange differences between her version and the official records.
  Could this be another clue to find the rumoured grandparents' vault ?

## Write-up
By looking at the example, you can deduct that the following methods have been used:

Temperature (°C) encodes letters (base temperature shifts after each letter by the last altered temperature value . The starting shift is 30).
Wind Speed (km/h) encodes numbers (base wind speed is 5 km/h, and it increases by 2 km/h for each subsequent number).
Humidity (%) encodes special characters (fixed base humidity of 40%, and each special character is encoded by adding its ASCII value mod 10).

Now you will have to compare the historical data with the given data and find the differences, because this incdicates that these lines contain code.
Then, step by step, decode as follows:

First line: temp has been changed => 37 (changed value) + 30 (base shift) = 67 (which corresponds to C in ASCII)
second line: nothing has been changed so ignore this line
third line: temp has been changes => 46 (changed value) + 37 (previous value) = 83 (which corresponds to S in ASCII)
<SNIP>
sixt line: humidity has been changed => humidity (43) = 40 + x mod 10 => possible values are 33 (!),43(+),63(?),93(]),123({) => since the standard format is CSC{} => the value will be 123({)
<SNIP>
eleventh line: humidity has been changed => humidity (45) = 40 + x mod 10 => possible values are 35(#),45(-),95(_),125(})
<SNIP>
20th line: windspeed has been changed => 0 times before has there been a number which was calculated => ((0*2)+5)+44(changed value)= 49 (which corresponds to 1 in ASCII)
<SNIP>
36th line: windspeed has been changed => 1 times before has there been a number which was calculated => ((1*2)+5)+42(changed value)= 49 (which corresponds to 1 in ASCII)
<SNIP>


## Solve script
PUT IT IN THE `Resources` FOLDER AND MENTION IT IN THE `healthcheck:` of `challenge.yml`

## Flag
CSC{I_Am_S1NGing_1N_Th3_V4Ul7}

## Creator
Sander Van Dessel

## Creator bio

