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
ENV FLAG "CSC{M0by_D1ck_W1ll_347_17_411}"
EXPOSE 80
ENTRYPOINT [ "/bin/bash", "/opt/pequod/run.sh" ]