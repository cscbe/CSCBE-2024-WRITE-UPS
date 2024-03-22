FROM python:3.7-slim-buster

RUN apt-get update -y \
    && apt-get install --no-install-recommends -y socat \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir "/opt/qr_frenzy"
COPY ./src/ "/opt/qr_frenzy/"
RUN pip install -r "/opt/qr_frenzy/requirements.txt"
WORKDIR "/opt/qr_frenzy/"
RUN chmod +x serve.sh server.py

ENV FLAG "CSC{qr_cOdE5_EvErywher3}"

EXPOSE 1338
CMD ./serve.sh