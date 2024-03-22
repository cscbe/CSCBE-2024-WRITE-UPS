# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory to /app
WORKDIR /app

# Copy the local directory contents into the container at /app
COPY . /app

# Expose port 1338
EXPOSE 1338

# Set flag
ENV FLAG="CSC{you_have_to_understand_most_people_are_not_ready_to_be_unplugged_35uf83js}"

# Run the Python script when the container launches
CMD ["python", "server.py"]
