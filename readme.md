# Robot Concepts
[![Build and Deploy](https://github.com/EganJ/robot-concepts/actions/workflows/gh-pages-deploy.yml/badh.sv?branch=main)]
(https://github.com/EganJ/robot-concepts/actions/workflows/gh-pages-deploy.yml)

View this website by visiting [eganj.github.io/robot-concepts/](https://eganj.github.io/robot-concepts/).

A collection of animations intended to be a visual aid when explaining robotics
concepts, primarily for an FRC audience. Animations created using 
[manim community](https://www.manim.community/).

## Workflows
### Task Management
Create issues for tasks that need to be done. Tasks can be anything from substantive
code retooling to requests for new animations to small visual tweaks. 

### Build
This repository includes a vs-code dev container. To open the repository in a dev container:
1. Install [docker desktop](https://www.docker.com/products/docker-desktop/).
2. Install [vs-code](https://code.visualstudio.com/download).
3. Add the **Dev Containers** extension to vs-code.
4. Open the command Palette (*Ctrl + Shift + P*), and run the *Dev Containers: Open Folder in Container* task. Select a folder containing a local copy of this repository.

Build the website by running either `make html` or the vs-code **build** task. 
Open the website by by running either `python -m http.server` or the vs-code **open** task and then opening [localhost:8000](localhost:8000/) in your web browser.