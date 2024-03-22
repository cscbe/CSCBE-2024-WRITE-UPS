FROM node:20.11.0
RUN mkdir /srv/app && chown node:node /srv/app
WORKDIR /srv/app
COPY src .
USER root
EXPOSE 80
RUN npm install
ENTRYPOINT [ "npx", "vite", "--host", "0.0.0.0" ]
