# Lesson 3 — Docker Images Optimization

## Objective

The goal of this assignment is to build and compare two Docker images for a machine learning inference application:

1. A **fat image** containing development tools and full runtime dependencies.
2. A **slim image** optimized for runtime using multi-stage builds.

The task demonstrates how container image size can be reduced by removing unnecessary dependencies and separating build and runtime environments.

---

## Project Description

The project contains a simple inference script using a pretrained PyTorch model.

The application loads an image and outputs the top predicted classes.

Example output:

Top predictions:
1. class_207: 0.8537  
2. class_852: 0.0055  
3. class_215: 0.0051  

---

## Fat Image

The fat image is built using `python:3.12` as a base image and includes additional development tools.

Installed packages include:

- curl
- wget
- git
- vim
- build-essential

These tools are useful during development but are not required in production.

The image also installs:

- PyTorch (CPU version)
- torchvision
- additional Python dependencies

### Build command

`docker build -f Dockerfile.fat -t ml-fat .`

### Run command

`docker run --rm ml-fat`

### Result

Image size: ml-fat: 2.16 GB


---

## Slim Image

The slim image uses a **multi-stage build**.

The first stage installs dependencies and creates a virtual environment.

The second stage uses `python:3.12-slim` and copies only the runtime environment and necessary application files.

This removes:

- development tools
- build dependencies
- unnecessary system libraries

### Build command

`docker build -f Dockerfile.slim -t ml-slim .`


### Run command

`docker run --rm ml-slim`


### Result

Image size: ml-slim: 1.12 GB


---

## Image Size Comparison

| Image | Size |
|------|------|
| ml-fat | 2.16 GB |
| ml-slim | 1.12 GB |


Size reduction:

2.16 GB → 1.12 GB

≈ 48% reduction


---

## Layer Analysis

Using `docker history` shows that the largest layer comes from the Python environment containing PyTorch and its dependencies.

Example layer:

COPY /opt/venv → ~982 MB


This demonstrates that machine learning frameworks are the primary contributor to container size.

---

## Additional Optimization

A `.dockerignore` file was added to prevent unnecessary files from being included in the build context.

This reduced the build context from approximately **1 GB to 19 MB**.

Ignored files include:

- `.venv`
- `__pycache__`
- `.git`
- temporary files

---

## Conclusion

The assignment demonstrates several important Docker practices:

- separating build and runtime environments
- using multi-stage builds
- reducing container image size
- excluding unnecessary files with `.dockerignore`

The optimized slim image reduced the size by nearly **50%** while maintaining the same functionality.

This approach improves deployment speed, reduces storage usage, and simplifies production environments.
