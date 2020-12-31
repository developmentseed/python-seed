
FROM confluentinc/cp-kafka:5.4.1

# Set the working directory to /app
WORKDIR .

# Copy the current directory contents into the container at /app
COPY . .

RUN chmod +x init.sh

CMD ./init.sh


