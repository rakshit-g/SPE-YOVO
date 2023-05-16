# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

RUN apt-get update && apt-get install -y python3-pil \ 
tesseract-ocr \
libtesseract-dev \
tesseract-ocr-eng \
tesseract-ocr-script-latn \
&& \
apt-get clean && \
rm -rf /var/lib/apt/lists/*

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000


# Run server.py when the container launches
CMD ["python", "server.py"]