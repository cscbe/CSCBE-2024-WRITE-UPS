FROM mcr.microsoft.com/playwright/python:next-jammy

WORKDIR /opt/app
RUN mkdir -p /opt/app
COPY src/ /opt/app/

RUN pip install -r requirements.txt

ENV FLAG="CSC{S0MEoN3_is_Alw4y5_waTch1N9}"

EXPOSE 80

ENTRYPOINT ["/opt/app/serve.sh"]
