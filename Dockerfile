# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install opencv-python
RUN pip install flask
RUN pip install flask_cors
RUN pip install PyYaml
RUN pip install ultralytics

# Make port available to the world outside this container
EXPOSE 5005

# Define environment variable
ENV NAME mining_safety_api

# Run app.py when the container launches
CMD ["python", "controller.py"]
