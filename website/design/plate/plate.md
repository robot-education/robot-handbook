# Plate

## Introduction

Flat plates are common structural components on many robots.

## Modeling

The basic process for modeling a plate is demonstrated in the following animation.

:::{animation} IntakePlateScene.mp4
:autoplay:
Sketching a basic plate
:::

Some considerations are as follows:

- Some CAD programs require trimming the circles into arcs before extruding.
- A curved exterior can be achieved by connecting circles using arcs instead of lines.
- If you prefer using the hole tool to extrude holes, skip drawing the inner circles or mark them as construction.
- In the event a hole is too close to the boundary of the circle, you may need to redraw the boundary.

:::{animation} BoundaryRedrawScene.mp4
Redrawing the boundary of a plate
:::

## Appendix

### Constraints

Lines should be constrained to each circle using coincident {{coincident}} and tangent {{tangent}}.

:::{animation} BoundaryConstraintScene.mp4
Constraining a boundary line
:::

Circles which are the same radius should be constrained together using equal {{equal}}.

<!-- ### Additional Examples -->
