# Easter Bunnies

## Category
Programming

## Estimated difficulty
Hard

## Description
Programming challenge based on a TEDx Youtube riddle.

## Scenario
The evil lord TED has captured all the Easter bunnies and their eggs. They are all chained and locked up. He has challenged them to a statistically impossible task. Fortunately for the bunnies, TED is not a strategist nor statistician.

## Write-up
Solution is based on this video: https://www.youtube.com/watch?v=vIdStMTgNl0

Odds of a chain being longer than 500 (for 1000 boxes) is ~30% => If every bunny follows his chain the odss that every one will succeed is 30% 
(In this challenge it is coded that it will always succeed)

Every bunny opens the box with his number. If it contains another number, go to that box. Continue this until you find your egg. 

Solve script included

Public file: this_must_mean_something.jpg
Includes a hint to "Youtube TEDx"

## Solve script
/Resources/solve_eggs.py

## Flag
CSC{the_lord_and_saviour_of_easter!!!_a_true_bunny_master!_175487548}

## Creator
Arnoud De Jonge

## Creator bio
As a Master of Science in Computer Science, I have taken an interest in cybersecurity. After finding joy in solving CTF challenges, I have taken pleasure in crafting thought-provoking challenges for participants of the following years. I hope you will love the challenges as much as you hate them, best of luck!
