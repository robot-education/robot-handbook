# FRC Animations

A collection of animations intended to be a visual aid when explaining robotics
concepts, primarily for an FRC audience. Animations created using 
[manim community](https://www.manim.community/)- check them out!

## Workflows

## Task Management
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

## Website
### Build
In order to build the website, you will need:
1. The build tool (Sphinx)[https://www.sphinx-doc.org/en/master/usage/installation.html]. On linux, run `sudo apt-get install -y python3-sphinx`.
2. The Read the Docs theme (sphinx-rtd-theme)[https://pypi.org/project/sphinx-rtd-theme/]. On linux, run `sudo apt-get install -y python3-sphinx-rtd-theme` (or `pip install sphinx-rtd-theme`?).

Once you've installed sphinx, you can build the website by running `make html`.
You can view the result by opening `build/html/index.html` in your web browser (using a command like `firefox build/html/index.html`).