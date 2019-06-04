# Use an official Python runtime as a parent image
FROM python:3.7-slim

# Copy the current directory contents into the container at /app
COPY requirements.txt /app/requirements.txt

# Set the working directory to /app
WORKDIR /app/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Enable python log on container
ENV PYTHONUNBUFFERED = 0
