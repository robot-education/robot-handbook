#!/bin/bash

# install dependencies
sudo apt-get update
# manim system libraries
sudo apt-get install -y build-essential libcairo2-dev libpango1.0-dev ffmpeg # texlive texlive-latex-extra

pip install --upgrade pip

# install pip requirements
pip install -r requirements.txt

# add the robot concepts helper library so we can import it anywhere
# this will install any packages specified in setup.py
pip install -e .