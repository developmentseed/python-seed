# Use an official Python runtime as a parent image
FROM python:3.7

# Set the working directory to /app
WORKDIR .

# Copy the current directory contents into the container at /app
COPY . .

COPY ../../isharp/datahub/web/templates /opt/templates


# Install any needed packages specified in requirements.txt
RUN pip install  --trusted-host pypi.python.org -r requirements.txt


RUN chmod +x init.sh


CMD ./init.sh


