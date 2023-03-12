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

### Creating a new animation
Using a Jupyter notebook can make prototyping animations much easier. Create a 
new notebook, add `from manim import *` to the top, and add the requisite 
ipython magic command to render the animation:

```python
# add once at the top to set the quality for all cells. Can be "ql", "qm", "qh", or "qk".
quality = "ql" 
```
```python
# add this to the cell that has the MyAnimation scene
%%manim -v WARNING --disable_caching -$quality MyAnimation
```

### Finalizing an animation
Haven't gotten this far yet. Jupyter notebooks are great for prototyping, but
not so great for building a library of tools and common code. Once an animation
prototype is pretty close to being done, we should figure out how to:
  - Move the animation-specific stuff into somewhere that makes sense
  - Organize any common code, like the `PIDSimulator` used by a `PIDScene`, into
    a library.

### Animation Dependencies
If we're going to be creating a common library used by multiple animations, do 
we want some way of tracking which animations depend on which tools so we can check
the output still works when we make changes to the tools?

### Build
This repository uses vs-code dev containers. To open the repository in a dev container:
1. Install [docker desktop](https://www.docker.com/products/docker-desktop/).
2. Install [vs-code](https://code.visualstudio.com/download).
3. Add the **Dev Containers** extension to vs-code.
4. Open the command Palette (*Ctrl + Shift + P*), and run the *Dev Containers: Open Folder in Container* task. Select a folder containing a local copy of this repository.

Build the website by running either `make html` or the vs-code **build** task. 
Open the website by by running either `python -m http.server` or the vs-code **open** task and then opening [localhost:8000](localhost:8000/) in your web browser.