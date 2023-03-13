# Plate
Plates are common components on many robots. Plates can be easily cut from sheets using a router or laser.

## Introduction
The basic process for modeling a plate is demonstrated in the following animation.
:::{figure} plate.gif
:alt: Drawing a plate
:width: 80%
:align: center
Sketching a simple plate
:::

Some considerations are as follows:
* Some CAD programs require trimming or deleting extraneous circles.
* A curved exterior may be achieved by connecting circles using arcs instead of lines.
* Many workflows specify that holes should be created using your CAD program's hole tool rather than extruding a circle. In this case, mark the inner circles as construction, and add the holes after sketching and extruding the plate.
* In the event a hole is too close to the boundary of the circle, you may need to redraw the boundary.
:::{figure} boundary_redraw.gif
:alt: Redrawing the boundary
:width: 80%
:align: center
Redrawing the boundary of the plate
:::

## Appendix
Lines should be constrained to each circle using both coincident and a tangent constraints.
:::{figure} boundary_constraints.gif
:alt: Constraining the boundary
:width: 80%
:align: center
Constraining a boundary line
:::