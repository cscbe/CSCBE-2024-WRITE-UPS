create self signed key

        openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -sha256 -days 3650 -nodes

build and run docker

        docker build -t outofbounds_server .
        docker run --init --rm -it -p 127.0.0.1:3000:3000 outofbounds_server