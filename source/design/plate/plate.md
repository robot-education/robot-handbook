# Plate
Plates are common components on many robots. Plates can be easily cut from sheets using a router or laser.

## Introduction
The basic process for modeling a plate is demonstrated in the following animation.
:::{figure} plate.mp4
:alt: Drawing a plate
:width: 80%
:align: center
Sketching a simple plate
:::

<video width="320" height="240">
    <source src="/_images/plate.mp4" type="video/mp4">
    Your browser does not support the video tag.
</video>

Some considerations are as follows:
* Your CAD program may require you to trim or delete circles before allowing you to finish your sketch.
* A curved exterior can be achieved by connecting circles using arcs instead of lines.
* Many users prefer creating 
* Many workflows specify that holes should be created using your CAD program's hole tool rather than extruding a circle. In this case, mark the inner circles as construction, and add the holes after sketching and extruding the plate.
* In the event a hole is too close to the boundary of the circle, you may need to redraw the boundary.

:::{figure} boundary_redraw.gif
:alt: Redrawing the boundary
:width: 80%
:align: center
Redrawing the boundary of the plate
:::

## Appendix
Lines should be constrained to each circle using both a coincident and a tangent constraint.
:::{figure} boundary_constraints.gif
:alt: Constraining the boundary
:width: 80%
:align: center
Constraining a boundary line
:::