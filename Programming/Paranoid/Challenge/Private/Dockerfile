# Use an official Python runtime as a parent image
FROM python:3.11-alpine

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY src /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV FLASK_APP=flask_server.py
ENV password="MonkeyBrain"
ENV flag="CSC{Al9ORi7hMic5_cLa22_Wa5_Co0L_aF73R_AlL}"

# Run app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0", "--port=80"]
