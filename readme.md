# Manim Dev Container
This branch features a stripped down vscode dev container useful for developing animations in manim.

This dev container comes with python 3.11 and manim as well as extensions and settings for developing
in python, jupyter notebook.

## Development
This repository includes a vs-code dev container. To open the repository:
1. Install [docker desktop](https://www.docker.com/products/docker-desktop/).
2. Install [vs-code](https://code.visualstudio.com/download).
3. Add the **Dev Containers** extension to vs-code.
4. Launch Docker Desktop on your computer.
5. Open the command Palette (*Ctrl + Shift + P*), and run the *Dev Containers: Open Folder in Container* task. Select a folder containing a local copy of this repository.

## Files
Python packages may be added to `requirements.txt`. Packages may be added to `setup.sh`.

If you make changes to `requirements.txt` or `setup.sh`, you'll need to rebuild the container or run `bash setup.sh` for the changes to apply.

## Build Script
This project includes a build script for compling animations with manim. The code is in `build.py`.
When used with the dev container, it can be run from the command line directly, e.g. `build`.
The build script includes a fuzzy matcher which will aggressively match inputs to targets. By default, `build` will build everything in `animations/`,
but individual paths, files, and scenes may be specified as well. For more information, run `build -h`.

### Examples
* Run `build` to build everything.
* Run `build -s MA` to build the scene `MovingAnimation`.
* Run `build -f ex` to build all scenes in `example.py`.
