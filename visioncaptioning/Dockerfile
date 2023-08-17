# Get the base Python Image from Docker Hub
FROM pytorch/torchserve:0.8.1-cpu

# Set the working directory to /app
WORKDIR /

# Copy the current directory contents into the container at /app
COPY visioncaptioning/requirements.txt .
ENV TRANSFORMERS_CACHE=visioncaptioning/models/models--Salesforce--blip-image-captioning-base

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY visioncaptioning/ visioncaptioning/

EXPOSE 5000

# Run app.py when the container launches
CMD ["python", "-m", "visioncaptioning.api"]