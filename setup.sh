#!/bin/bash

# install dependencies
sudo apt-get update
# manim system libraries
sudo apt-get install -y build-essential libcairo2-dev libpango1.0-dev ffmpeg # texlive texlive-latex-extra

# install command line utilities
sudo apt-get install -y man vim less

# install pip requirements
pip install -r requirements.txt