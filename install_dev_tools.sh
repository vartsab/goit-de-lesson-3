#!/bin/bash

echo "Installing development tools..."

sudo apt update

sudo apt install -y \
    docker.io \
    docker-compose \
    git \
    curl \
    wget \
    vim

echo "Installation completed."
