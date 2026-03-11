# ML Inference Docker Example

This project demonstrates building and optimizing Docker images for a machine learning inference application.

Two Docker images are provided:

- **Fat image** — includes development tools and full dependencies.
- **Slim image** — optimized runtime image using multi-stage builds.

---

## Project Structure

Dockerfile.fat
Dockerfile.slim
requirements.txt
inference.py
model.pt
sample.png
report.md


---

## Build Fat Image

`docker build -f Dockerfile.fat -t ml-fat .`


Run:

`docker run --rm ml-fat`


---

## Build Slim Image

`docker build -f Dockerfile.slim -t ml-slim .`


Run:

`docker run --rm ml-slim`


---

## Expected Output


Top predictions:

class_207: 0.8537

class_852: 0.0055

class_215: 0.0051


---

## Image Sizes

| Image | Size |
|------|------|
| ml-fat | ~2.16 GB |
| ml-slim | ~1.12 GB |

The slim image is nearly **50% smaller** due to the use of multi-stage builds and removal of development dependencies.

---

## Author

Denys Vartsab
