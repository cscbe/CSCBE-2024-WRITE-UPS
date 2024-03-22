FROM python:3.8-slim-buster
EXPOSE 80
ENV flag "CSC{th3_f0unt41n_0f_y00th}"
COPY ./requirements.txt /var/www/requirements.txt
COPY ./app /app
COPY ./database.db /var/www/database.db
RUN chmod 777 /var/www/database.db
WORKDIR /app
RUN pip install -r /var/www/requirements.txt
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0","--port=80"]
