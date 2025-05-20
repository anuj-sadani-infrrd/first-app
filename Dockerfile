# Base image: Using a full Ubuntu image unnecessarily
FROM ubuntu:20.04

# Install Python manually (slow + large image size)
RUN apt update && \
    apt install -y python3 python3-pip git wget

# Install all packages at once, no caching or pinning
COPY requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt

# Copy the full codebase without a .dockerignore file
COPY . /app

# Set working directory (too late in the process)
WORKDIR /app

# Run the app (bad: uses python3 directly, no entrypoint, no logging config)
CMD ["python3", "main.py"]
