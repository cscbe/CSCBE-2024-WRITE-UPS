# Environmental Hazard

## Category
Reversing

## Estimated difficulty
Easy

## Description
UPX 3.94 packed go binary

## Scenario
  Oh no!
  
  My flag-holding program walked onto a wet floor, and dropped the flag :(
  
  It needs some help, would you be so kind as to get it yourself?

## Write-up
use strings on the binary, to figure out it's UPX

From there, you can try multiple solutions, such as
- Unpacking with UPX 3.94
- Using the multitude of upx unpacking projects online
- Debug the program after it gets decompressed to find the flag in memory (https://infosecwriteups.com/how-to-unpack-upx-packed-malware-with-a-single-breakpoint-4d3a23e21332)

## Solve script
PUT IT IN THE `Resources` FOLDER AND MENTION IT IN THE `healthcheck:` of `challenge.yml`

## Flag
CSC{Y3AH_upX_15_n0T_S3cURitY}

## Creator
Théo Davreux

## Creator bio
blaehgh