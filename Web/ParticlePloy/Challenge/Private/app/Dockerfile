FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt /app
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt

COPY . /app

## Copy the current directory contents into the container at /app
#COPY .. /app

# Make port 5000 available to the world outside this container
EXPOSE 5000


#ENTRYPOINT ["python3"]
#CMD ["app.py"]

# Run app.py when the container launches
CMD ["flask", "--app", "app", "--debug", "run", "--host", "0.0.0.0", "--port", "8080"]

