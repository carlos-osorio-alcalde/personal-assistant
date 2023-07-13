# Get the base Python Image from Docker Hub
FROM python:3.10.6

# Set the working directory to /app
WORKDIR /

# Copy the current directory contents into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY assistantbot/ assistantbot/
COPY main.py .
COPY .env .

# Run app.py when the container launches
CMD ["python", "main.py"]

