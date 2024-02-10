# Plate

## Introduction
Flat plates are common structural components on many robots. 

## Modeling
The basic process for modeling a plate is demonstrated in the following animation.

:::{animation} IntakePlateScene.mp4
Sketching a basic plate
:::

Some considerations are as follows:
* Some CAD programs require trimming the circles into arcs before extruding.
* A curved exterior can be achieved by connecting circles using arcs instead of lines.
* If you prefer to use the hole tool to extrude holes, skip drawing the inner circles.
<!-- * Many workflows specify that holes should be created using your CAD program's hole tool rather than extruding a circle. In this case, mark the inner circles as construction, and add the holes after sketching and extruding the plate. -->
* In the event a hole is too close to the boundary of the circle, you may need to redraw the boundary.

:::{animation} BoundaryRedrawScene.mp4
Redrawing the boundary of a plate
:::

## Appendix
### Constraints
Lines should be constrained to each circle using a coincident {{coincident}} constraint and a tangent {{tangent}} constraint.

:::{animation} BoundaryConstraintScene.mp4
Constraining a boundary line
:::

Circles which are the same radius should be constrained together using equal {{equal}} constraints.

<!-- ### Additional Examples -->