# Get the base Python Image from Docker Hub
FROM python:3.10.6

# Set the working directory to /app
WORKDIR /

# Copy the current directory contents into the container at /app
COPY expenses/requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY expenses/ expenses/

# Expose the port
EXPOSE 5000

# Run app.py when the container launches
CMD ["python", "-m", "expenses.main"]