# Plate
Plates are common components on many robots. Plates can be easily cut from sheets using a router or laser.

## Introduction
The basic process for modeling a plate is demonstrated in the following animation.
<!-- :::{figure} plate.mp4
:alt: Drawing a plate
:width: 80%
:align: center
Sketching a simple plate
::: -->

:::{animation} IntakePlateScene.mp4
    :size: standard
    :loop:
    :autoplay:
    Some text
:::

<figure class="align-center" id="id1">
<a class="reference internal image-reference" href="video/plate.mp4">
    <video width="80%" controls>
        <source src="video/plate.mp4" type="video/mp4">
        Drawing a plate
    </video>
</a>
<figcaption>
<p><span class="caption-text">Sketching a plate</span><a class="headerlink" href="#id1" title="Permalink to this image"></a></p>
</figcaption>
</figure>

Some considerations are as follows:
* Your CAD program may require you to trim or delete circles before allowing you to finish your sketch.
* A curved exterior can be achieved by connecting circles using arcs instead of lines.
* Many users prefer creating 
* Many workflows specify that holes should be created using your CAD program's hole tool rather than extruding a circle. In this case, mark the inner circles as construction, and add the holes after sketching and extruding the plate.
* In the event a hole is too close to the boundary of the circle, you may need to redraw the boundary.

<!-- :::{figure} boundary_redraw.gif
:alt: Redrawing the boundary
:width: 80%
:align: center
Redrawing the boundary of the plate
::: -->

## Appendix
Lines should be constrained to each circle using both a coincident and a tangent constraint.
<!-- :::{figure} boundary_constraints.gif
:alt: Constraining the boundary
:width: 80%
:align: center
Constraining a boundary line
::: -->

<!-- <figure class="align-center" id="id1">
<a class="reference internal image-reference" href="design/plate/boundary_constraints.gif"><img alt="Constraining the boundary" src="design/plate/boundary_constraints.gif" style="width: 80%;" /></a>
<figcaption>
<p><span class="caption-text">Constraining a boundary line</span><a class="headerlink" href="#id1" title="Permalink to this image"></a></p>
</figcaption>
</figure> -->