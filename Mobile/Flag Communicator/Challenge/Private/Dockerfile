FROM python:3.12

COPY server.py ./server.py
COPY cert.pem ./cert.pem
COPY key.pem ./key.pem

ENV FLAG="CSC{b1g_5n4CC_foR_th4_3VI1_ST4cc!}"
ENV PYTHON_PORT=443
EXPOSE 443

CMD [ "python3", "./server.py" ]
