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