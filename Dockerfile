# Use a lightweight Perl & Python image
FROM perl:latest

# Install necessary dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    git \
    && apt-get clean

# Install required Perl modules
RUN cpanm Image::PHash

# Set working directory
WORKDIR /app

# Copy scripts into the container
COPY deduplicate.py /app/deduplicate.py
COPY phash.pl /app/phash.pl

# Ensure /images directory exists
RUN mkdir -p /images

# Set a volume for images
VOLUME ["/images"]

# Set the command to run the Python script
CMD ["python3", "/app/deduplicate.py"]
