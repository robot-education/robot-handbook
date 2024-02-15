# Robot Concepts

[![Build and Deploy](https://github.com/robot-education/robot-handbook/actions/workflows/deploy-website.yaml/badge.svg?branch=main)](https://github.com/robot-education/robot-handbook/actions/workflows/deploy-website.yaml)

View the website by visiting [robothandbook.dev](https://robothandbook.dev).

Robot Concepts is a collection of animations and other documentation intended to be a visual aid when explaining robotics
concepts, primarily for an FRC audience. Animations created using [manim community](https://www.manim.community/).

<!-- ## Development
This repository includes a vs-code dev container. To open the repository:
1. Install [docker desktop](https://www.docker.com/products/docker-desktop/).
2. Install [vs-code](https://code.visualstudio.com/download).
3. Add the **Dev Containers** extension to vs-code.
4. Open the command Palette (*Ctrl + Shift + P*), and run the *Dev Containers: Open Folder in Container* task. Select a folder containing a local copy of this repository. -->

### Build

Individual animations in `source` may be compiled using the build script defined in `library/build.py`. To build every animation as low quality, run `build` from the command line.
Run `build --help` to see additional information on how to compile specific paths, files, or animations. Built animations will be inserted into a `media` folder next to the generating file in `website`.

The website can be built by running the vs-code **dev-server** task and opening [localhost:8000](http:://localhost:8000) in your web browser.
