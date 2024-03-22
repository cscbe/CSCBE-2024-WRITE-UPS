FROM mcr.microsoft.com/playwright/python:v1.42.0-jammy

RUN adduser \
    --disabled-login \
    -u 1001 \
    --gecos "" \
    --shell /bin/bash \
    app
WORKDIR /opt/app
RUN mkdir -p /opt/app

COPY src/ /opt/app/
RUN pip install -r requirements.txt
RUN chown -R 1001:1001 /opt/app && chmod -R 755 /opt/app

RUN apt update && apt upgrade -y

RUN apt install nginx -y

RUN apt install sudo -y

COPY src/nginx-default /etc/nginx/sites-available/default
COPY src/app-nginx-sudo /etc/sudoers.d/app-nginx-sudo

ENV FLAG="CSC{y3ah_D0N't_us3_uuid_v1}"

USER 1001
EXPOSE 80
ENTRYPOINT ["/opt/app/serve.sh"]
