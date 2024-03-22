FROM python:alpine

RUN apk update && apk add bash firefox

WORKDIR /code

COPY ./app/requirements.txt /code/app/
COPY ./admin-simulation/requirements.txt /code/admin-simulation/
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r app/requirements.txt -r admin-simulation/requirements.txt

COPY . /code

# Make port 5000 available to the world outside this container
EXPOSE 80

ENV FLAG=CSC{In_7HE_d3PtH_Of_tHe_d0m_name5_HOld_p0WeR}

CMD ["bash", "wrapper-entrypoint.sh"]
