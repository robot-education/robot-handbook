# Feature Dialogs

:::{note} This page is specific to Onshape. It is unlikely to apply to other CAD software.
:::

This page discusses some important features of Onshape feature dialogs and provides tips and tricks to avoid falling into some common pitfalls associated with them.

Feature dialogs refers to menus that open whenever a feature is edited in Onshape. They are used all across Onshape, including in Part Studios, Assemblies, and Drawings.

<!-- A feature dialog in an assembly. -->

## Working With Selection Parameters

Many Onshape features have multiple places where selections can be made. For example, the Mirror feature requires both selecting features/parts to extrude as well as a plane to mirror about. In these cases, you must first specify exactly where you'd like your selections to go by first clicking the appropriate Selection parameter.

<!-- Gif of managing parameter focus to fill out an assembly mirror -->

Onshape will automatically filter selections in the Graphics window to the type of the current active Selection parameter. So, it isn't possible to select a mirror plane while the **Parts to mirror** Selection parameter is active, and vice-versa for parts while the **Mirror plane** Selection parameter is active.

:::{warning}
If you're trying to make a selection you need but Onshape is refusing to highlight it, double check that the right Selection parameter is active!
:::

## Selecting An Entire Sketch

When you click a sketch in the feature tree, Onshape will automatically create a query which will always use all elements from that sketch.

This can be faster than manually selecting every sketch element one-by-one, and is more robust to future changes to the sketch (since changes to the sketch will be automatically reflected in the feature).

:::{tip} When you create an Extrude or Revolve directly from inside a sketch, Onshape will select the entire sketch for you automatically.
:::

## Troubleshooting Features

When Features are in an invalid state, they will turn red in the Feature tree. When a feature is in this state, an error message will be made available.

<!-- Screenshots of hovering over the error message in the tooltip/feature dialog -->

Some features will also display banner messages, mark specific parameters in red, and show various error geometry while they are open.

For example, the Hole tool will show the holes it is attempting to cut when one or more Sketch points are selected and the Merge scope is empty.

<!-- Screenshot of hole tool error bodies -->

## Extrude Editing Logic

Several Onshape features use editing logic which automatically triggers to make updates to various parameters in response to input from the user. For example, features like the Hole tool will attempt to automatically fill in their merge scope when a selection is made.

<!-- Insert gif of hole tool merge scope getting filled in automatically -->

This behavior is generally helpful, but it can be detrimental in the case of the Extrude feature, which likes to automatically set itself to **Add** when a selection is made which is adjacent to another part.

<!-- Insert gif of Extrude setting itself to Add -->

If you do not want Onshape to join your extrude with another part, you should keep an eye out for this behavior. If it does happen, you can fix it by toggling your extrude back to **New**.

:::{warning}
If you're expecting to have multiple parts but you only have one, double check that Onshape hasn't automatically changed your extrude to **Add**!
:::
