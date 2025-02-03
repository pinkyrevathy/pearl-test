# Overview

This project provides an automated way to detect and remove duplicate images using perceptual hashing. The implementation consists of a Python script, a Dockerized environment, and a GitHub Actions workflow to automate deduplication when new images are added.

# Features

Identifies duplicate images using perceptual hashing .

Moves duplicates to a duplicates/ directory (optional deletion mode available).

Automated GitHub Actions Workflow to process images upon push.

# Installation

1️⃣ Local Setup

Prerequisites:

Python 3.9+

pip install -r requirements.txt

Run deduplication:

python deduplicate.py

2️⃣ Dockerized Setup

Build the Docker Image:

> ```
> docker build -t phash-automated .
> ```

Run the container:

> ```
> docker run --rm -v $(pwd)/images:/app/images phash-automated
> ```

# How It Works

The script scans image folders (images/) and generates perceptual hashes.

If two images have the same hash, they are considered duplicates.

The duplicate images are moved to a duplicates/ folder.

# GitHub Actions Workflow

The .github/workflows/image-deduplication.yml file automates the process.

When new images are added and pushed, the workflow:

Runs deduplicate.py.

Moves duplicates into duplicates/.

Commits & pushes changes back to the repo.

# Trigger

Runs only when images change:

> ```
> on:
>  push:
>    branches:
>      - main
>      - feature/** 
>    paths:
>      - "images/**"
> ```

Example Output 

> ```
> Cutting duplicate: images/team/20188f8d21b20153.jpg to images/team/duplicates/20188f8d21b20153.jpg
> Cutting duplicate: images/team/201334e8fdc62e76.jpg to images/team/duplicates/201334e8fdc62e76.jpg
> ```

# Improvements

1. Adding PAT token instead of Github Token
2. Make the code to work on any other types of images like png etc
3. phash.pl file is not used

# How to use this repository

1. Create a feature branch. 
2. Add the images which we want to check for duplicates
3. Raise a Pull Request and merge to master
4. On PR, github workflow is trigerred and on success the code is committed back to master repo.
5. On failure, the code is not merged.
