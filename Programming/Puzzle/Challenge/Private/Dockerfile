FROM python:3.11

RUN apt-get update -y \
    && apt-get install --no-install-recommends -y socat \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY ./src/ /opt/app/
WORKDIR /opt/app/

RUN pip install -r "/opt/app/requirements.txt"
RUN chmod +x serve.sh

ENV FLAG "CSC{wOw_th4NKs_My_NiEce_iS_happy_Now}"

EXPOSE 1337
CMD /opt/app/serve.sh
