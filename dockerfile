# Use the official Python image as the base image
FROM python:3.9-slim

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . .

# Expose port 8443
EXPOSE 8443

# Command to run the Flask application
CMD ["flask", "run", "--port=8443"]
