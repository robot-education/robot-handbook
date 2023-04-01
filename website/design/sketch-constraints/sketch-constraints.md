---
myst:
    substitutions:
        coincident_title: "![coincident](/design/images/coincident.svg){.thumbnail} Coincident (i)"
        vertical_title: "![vertical](/design/images/vertical.svg){.thumbnail} Vertical (v)"
        horizontal_title: "![horizontal](/design/images/horizontal.svg){.thumbnail} Horizontal (h)"
        parallel_title: "![parallel](/design/images/parallel.svg){.thumbnail} Parallel (b)"
        perpendicular_title: "![perpendicular](/design/images/perpendicular.svg){.thumbnail} Perpendicular"
        equal_title: "![equal](/design/images/equal.svg){.thumbnail} Equal (e)"
        midpoint_title: "![midpoint](/design/images/midpoint.svg){.thumbnail} Midpoint"
        tangent_title: "![tangent](/design/images/tangent.svg){.thumbnail} Tangent (t)"
        concentric_title: "![concentric](/design/images/concentric.svg){.thumbnail} Concentric"
---

# Sketch Constraints
This tutorial provides a visual guide to the behavior of various constraints. Although the constraint icons and shortcuts are for Onshape, the selections and behaviors are generally applicable to all CAD software.

## {{coincident_title}}
The coincident constraint is used to make points touch other entities. The available modes are:
* Two points - the points become touching.
:::{animation} CoincidentPointsScene.mp4
:autoplay:
Applying coincident {{coincident}} to points
:::

* A point and a line, circle or arc - the point becomes inline with the path of the line, circle, or arc.

:::{animation} CoincidentPointLineScene.mp4
:autoplay:
Applying coincident {{coincident}} to a point and a line or circle
:::

:::{note} This mode treats arcs as circles and lines as infinite, so points are not required to lie within the physical limits of the edge.
:::

* [Two lines - the lines become inline with each other.]{#coincident-two-lines}

:::{animation} CoincidentLineScene.mp4
:autoplay:
Applying coincident {{coincident}} to lines
:::

## {{vertical_title}}
The vertical constraint is used to make lines or pairs of points vertical relative to the sketch plane. The available modes are:
* Line - the line becomes vertical.

:::{animation} VerticalLineScene.mp4
:autoplay:
Applying vertical {{vertical}} to a line
:::

* Two points - the points become vertically inline with each other.

:::{animation} VerticalPointsScene.mp4
:autoplay:
Applying vertical {{vertical}} to two points
:::

## {{horizontal_title}}
The vertical constraint is used to make lines or pairs of points horizontal relative to the sketch plane. The available modes are:
* Line - the line becomes horizontal.

:::{animation} HorizontalLineScene.mp4
:autoplay:
Applying horizontal {{horizontal}} to a line
:::

* Two points - the points become horizontally inline with each other.

:::{animation} HorizontalPointsScene.mp4
:autoplay:
Applying horizontal {{horizontal}} to two points
:::

## {{parallel_title}}
The parallel constraint is used to make lines parallel to each other, meaning they point in the same direction. The available mode is:
* Two lines - the lines become parallel.

:::{animation} ParallelScene.mp4
:autoplay:
Applying parallel {{parallel}} to two lines
:::


:::{note} Parallel {{parallel}} makes lines share the same direction, but it does not force them to be inline with each other. 
    To make two lines parallel and inline, use [coincident {{coincident}} with two lines](#coincident-two-lines).
:::

## {{perpendicular_title}}
The perpendicular constraint is used to make lines perpendicular to each other, meaning they are at right angles relative to each other. The available mode is:
* Two lines - the lines become perpendicular to each other.

:::{animation} PerpendicularScene.mp4
:autoplay:
Applying perpendicular {{perpendicular}} to two lines
:::


## {{equal_title}}
The equal constraint is used to constrain the lengths of lines or the radius of arcs/circles to be the same. The available modes are:
* Two lines - the length of each line becomes the same.

:::{animation} EqualLineScene.mp4
:autoplay:
Applying equal {{equal}} to lines
:::

* Two circles or arcs - the radius of each circle or arc becomes the same.

:::{animation} EqualCircleScene.mp4
:autoplay:
Applying equal {{equal}} to circles and arcs
:::

:::{tip} Equal {{equal}} may be applied to multiple entities at once by preselecting multiple entities before clicking {{equal}}.
:::

## {{midpoint_title}}
The midpoint constraint is used constrain points to lie along the center of a line or between two other points. The available modes are:
* A point and a line - the point is placed in the middle of the line.

:::{animation} MidpointLineScene.mp4
:autoplay:
Applying midpoint {{midpoint}} to points and lines
:::

* Three points - the middle point is centered between the other two points.

:::{animation} MidpointPointScene.mp4
:autoplay:
Applying midpoint {{midpoint}} to points
:::

:::{tip} The order of selection does not matter, only the relative position of the points prior to midpoint {{midpoint}} being added.
:::


## {{tangent_title}}
The tangent constraint is used to make lines tangent to a circle or arc. A line is tangent when its edge touches the circle at a single point. The available modes are:
* A line and a circle or arc - the line becomes tangent to the circle or arc.

:::{animation} TangentLineScene.mp4
:autoplay:
Applying tangent {{tangent}} to lines and a circle
:::

* Two circles or arcs - The circles or arcs become tangent to one another.

:::{animation} TangentCircleScene.mp4
:autoplay:
Applying tangent {{tangent}} to circles and arcs
:::

## {{concentric_title}}
The concentric constraint makes circular entities share the same center point. The available modes are:
* Two circles or arcs - the centers of the circles or arcs become coincident.

:::{animation} ConcentricEdgeScene.mp4
:autoplay:
Applying concentric {{concentric}} to circles and arcs
:::

* A point and a circle or arc - the point becomes coincident to the center of the circle or arc.

:::{animation} ConcentricPointScene.mp4
:autoplay:
Applying concentric {{concentric}} to points
:::

<!-- * Two points - the points become coincident. -->