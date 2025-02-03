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
COPY bin/phash.pl /app/bin/phash.pl

# Ensure phash.pl is executable
RUN chmod +x /app/bin/phash.pl

# Ensure /images directory exists
RUN mkdir -p /images

# Initialize Git repo in container
RUN git init /images && \
    cd /images && \
    git config --global user.email "pinkyrevathy@gmail.com" && \
    git config --global user.name "GitHub Actions"

# Set a volume for images
VOLUME ["/images"]

# Set the command to run the Python script
CMD ["python3", "/app/deduplicate.py"]
