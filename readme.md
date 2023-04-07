# Robot Concepts
This branch features a stripped down dev-container useful for developing animations in manim.
Using a dev container makes it much easier to reliably write animations in a fixed environment.

## Development
This repository includes a vs-code dev container. To open the repository:
1. Install [docker desktop](https://www.docker.com/products/docker-desktop/).
2. Install [vs-code](https://code.visualstudio.com/download).
3. Add the **Dev Containers** extension to vs-code.
4. Open the command Palette (*Ctrl + Shift + P*), and run the *Dev Containers: Open Folder in Container* task. Select a folder containing a local copy of this repository.

When the dev container is opened for the first time, it is expected for the code to run for some time. 

## Files
Python packages may be added to `requirements.txt`. Packages may be added to `setup.sh`.

If you make changes to `requirements.txt` or `setup.sh`, you'll need to rebuild the container or run `bash setup.sh` for the changes to apply.

## Build Script
This project includes a build script for 