FROM node:16-alpine3.16

ENV LANG="C.UTF-8" 
ENV PUPPETEER_SKIP_DOWNLOAD=true

RUN apk update && \
    apk add --no-cache zlib-dev udev nss ca-certificates chromium && \
    adduser -h /home/admin-bot -D -u 10086 admin-bot && \
    yarn cache clean && \
    rm -rf /tmp/* /etc/apk/* /var/cache/apk/* /usr/share/man

WORKDIR /home/admin-bot

COPY ./*.json .

USER admin-bot

RUN npm install

COPY . .

CMD ["node", "/home/admin-bot/index.js"]