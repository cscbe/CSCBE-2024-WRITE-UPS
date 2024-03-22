# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory to /app
WORKDIR /app

# Copy the local directory contents into the container at /app
COPY . /app

# Expose port 1740
EXPOSE 1339

# Set flag (needs to be shorter than 100 characters)
ENV FLAG="CSC{Wh1sp3ring_fl4gs_w1th_High_pri0r1ty}"

# Run the Python script when the container launches
CMD ["python", "server.py"]
