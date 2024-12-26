# Use Debian slim base image
FROM debian:11-slim

# Install necessary packages and Python
RUN apt-get update && apt-get install -y --no-install-recommends \
    cmake g++ python3 python3-pip python3-venv && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app
ENV CXX=g++
COPY . .
RUN pip3 install --no-cache-dir .

