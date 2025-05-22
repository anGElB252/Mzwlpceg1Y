# Use the official Python image as the base image
FROM python:3.10-slim-bullseye

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .
# Install the required python pakages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the working directory
COPY . .

# set the environment variables for the flask app
ENV FLASK_RUN_HOST=0.0.0.0

# Expose the port on which the flask app will run
EXPOSE 5000

# Start the Flask app when the container is run
CMD ["flask", "run"]