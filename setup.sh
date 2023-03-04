#!/bin/bash

# install dependencies
sudo apt-get update
sudo apt-get install -y build-essential python3-dev libcairo2-dev libpango1.0-dev ffmpeg texlive

# install pip requirements
pip install -r requirements.txt