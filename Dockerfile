# Use an official Python runtime as a parent image
FROM python:3.7-slim

# Copy the current directory contents into the container at /app
COPY ["blockchainNode", "/app/blockchainNode"]
COPY ["blockchainClient", "/app/blockchainClient"]
COPY ["requirements.txt", "/app/requirements.txt"]

# Set the working directory to /app
WORKDIR /app/

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Set the working directory to /app/blockchainNode
WORKDIR /app/blockchainNode

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
#ENV NAME World

# Run app.py when the container launches
CMD ["python", "manage.py", "runserver" ,"0.0.0.0:80"]
