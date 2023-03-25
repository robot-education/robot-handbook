---
myst:
    substitutions:
        coincident: "![coincident](images/coincident.svg){.thumbnail}"
        vertical: "![vertical](images/vertical.svg){.thumbnail}"
        horizontal: "![horizontal](images/horizontal.svg){.thumbnail}"
        parallel: "![parallel](images/parallel.svg){.thumbnail}"
        perpendicular: "![perpendicular](images/perpendicular.svg){.thumbnail}"
        equal: "![equal](images/equal.svg){.thumbnail}"
        midpoint: "![midpoint](images/midpoint.svg){.thumbnail}"
        tangent: "![tangent](images/tangent.svg){.thumbnail}"
        coincentric: "![coincentric](images/coincentric.svg){.thumbnail}"
---

# Sketch Constraints
This tutorial provides a visual guide to the behavior of various constraints. Although the constraint icons and shortcuts are for Onshape, most of the behavior is identical for other CAD software.

## {{coincident}} Coincident Constraint (i) 

* Two points - the points become touching.

    :::{animation} CoincidentPointToPointScene.mp4
        :autoplay:
        Applying a coincident constraint to two points
    :::

* A point and a line, circle or arc - the point becomes inline with the path of the line, circle, or arc.

    :::{animation} CoincidentPointToLineScene.mp4
        :autoplay:
        Applying a coincident constraint to a point and a line or circle
    :::

    :::{note} This mode treats arcs as circles and lines as infinite, so points are not required to lie within the physical limits of the edge.
    :::

* Two lines - the lines become inline with each other.

    :::{animation} CoincidentLineToLineScene.mp4
        :autoplay:
        Applying a coincident constraint to two lines
    :::

## {{vertical}} Vertical Constraint (v)
* Line - the line becomes vertical.

* Two points - the points become vertically inline with each other.


## {{horizontal}} Horizontal Constraint (h)
* Line - the line becomes horizontal.
* Two points - the points become horizontally inline with each other.

## {{parallel}} Parallel Constraint (b)
* Two lines - the lines become parallel.

## {{perpendicular}} Perpendicular Constraint
* Two lines - the lines become perpendicular to each other. 

## {{equal}} Equal Constraint (e)
* Two or more lines - the length of each line becomes the same.
* Two or more circles or arcs - the radius of each circle or arc becomes the same.

## {{midpoint}} Midpoint Constraint
* A point and a line - the point is placed in the middle of the line.

* Three points - the middle point is centered between the other two points.
:::{tip} The order of selection does not matter.
:::


## {{tangent}} Tangent Constraint (t)
* A line and a circle or arc - the line becomes tangent to the circle or arc.

* Two circles or arcs - The circles or arcs become tangent to one another.


## {{coincentric}} Coincentric Constraint
* Two circles or arcs - the circles or arcs share the same center point.

<!-- # Appendix
## Additional Examples -->