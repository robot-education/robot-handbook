# Sketch Constraints
This tutorial provides a visual guide to the behavior of various constraints.

## Terminology
Most sketch entities have additional points associated with them in addition to their edges. 
For example, the sketch line command creates a line with a control point at either end. 
Constraining one of the control points results in different behavior compared to constraining the line itself.

## Constraints
### Coincident Constraint (i)
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

    :::{note} This mode does not guarantee that a point will lie on a given line or arc, just that it is inline with one.
    :::

* Two lines - the lines become inline with each other.

    :::{animation} CoincidentLineToLineScene.mp4
        :autoplay:
        Applying a coincident constraint to two lines
    :::

<!-- :::{figure} images/coincident.svg
:alt: Redrawing the boundary
:width: 60%
:align: center
Redrawing the boundary of the plate
::: -->

### Vertical Constraint (v)
* Line - the line becomes vertical.

* Two points - the points become vertically inline with each other.


### Horizontal Constraint (h)
* Line - the line becomes horizontal.
* Two points - the points become horizontally inline with each other.

### Parallel Constraint (b)
* Two lines - the lines become parallel.

### Perpendicular Constraint
* Two lines - the lines become perpendicular to each other. 

### Equal Constraint (e)
* Two or more lines - the length of each line becomes the same.
* Two or more circles or arcs - the radius of each circle or arc becomes the same.

### Midpoint Constraint
* A point and a line - the point is placed in the middle of the line.

* Three points - the middle point is centered between the other two points.
:::{tip} The order of selection does not matter.
:::


### Tangent Constraint (t)
* A line and a circle or arc - the line becomes tangent to the circle or arc.

* Two circles or arcs - The circles or arcs become tangent to one another.


### Coincentric Constraint
* Two circles or arcs - the circles or arcs share the same center point.

<!-- # Appendix
## Additional Examples -->