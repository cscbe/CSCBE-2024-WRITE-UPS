FROM python:3.8.10
RUN apt update && apt install nginx sudo -y
COPY ./nginx_config/nginx-conf /etc/nginx/nginx.conf
COPY ./nginx_config/nginx-default /etc/nginx/sites-available/default
COPY ./nginx_config/nginx-sudo /etc/sudoers.d/nginx-sudo
COPY ./src/requirements.txt /tmp/requirements.txt
RUN python3 -m pip install -r /tmp/requirements.txt
COPY ./src /opt/pequod
WORKDIR /opt/pequod
RUN chmod +x run.sh
RUN useradd gunicornrunner
RUN chown -R gunicornrunner:gunicornrunner repository
USER gunicornrunner
EXPOSE 80
ENV FLAG "SCS{This is not the flag, but it's where the flag would be. Don't try to turn it in. I will know. This will be disappointing if you do. Seriously. Don't do it.}"
ENTRYPOINT [ "/bin/bash", "/opt/pequod/run.sh" ]