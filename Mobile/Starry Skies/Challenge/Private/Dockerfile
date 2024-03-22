FROM python:3.12

COPY server.py ./server.py
COPY cert.pem ./cert.pem
COPY key.pem ./key.pem
COPY ca-cert.pem ./ca-cert.pem

ENV FLAG="CSC{pr0f1l3_Th1S_You_fi11hy_c45UA7}"
ENV PYTHON_PORT=443
EXPOSE 443

CMD [ "python3", "./server.py" ]
