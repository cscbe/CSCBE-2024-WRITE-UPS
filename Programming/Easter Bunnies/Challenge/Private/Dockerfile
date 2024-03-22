FROM python:3.10-slim-buster

RUN apt-get update -y \
    && apt-get install --no-install-recommends -y socat \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir "/opt/easter_bunnies"
COPY ./src/* "/opt/easter_bunnies/"
RUN pip install -r "/opt/easter_bunnies/requirements.txt"
WORKDIR "/opt/easter_bunnies/"
RUN chmod +x serve.sh bunnies.py

EXPOSE 1338
CMD ./serve.sh
