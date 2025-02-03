# Use a lightweight Perl & Python image
FROM perl:latest

# Install required Perl modules
RUN cpanm Image::PHash

# Install Python and dependencies
RUN apt-get update && apt-get install -y python3 python3-pip python3-venv

# Set the working directory
WORKDIR /app

# Create a virtual environment
RUN python3 -m venv /app/
