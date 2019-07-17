FROM jupyter/scipy-notebook


# Set the working directory to /app
WORKDIR .

# Copy the current directory contents into the container at /app
COPY . .



RUN pip install --trusted-host pypi.python.org -r requirements.txt

