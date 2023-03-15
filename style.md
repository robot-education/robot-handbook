# Style
This document describes the style guide for the website and animations.

# Animations
## Timing
Avoid running animations with non-standard units of time. Prefer using one of the following values:
`0, 0.25, 0.5, 0.75, 1, 1.5, 2, 2.5, 3, 4, 5...`
When setting the pace of an animation, consider that animations may play in a format which is not easily
pausable, and that many users prefer a slower format. 

Animations should always finish with a delay equal to `END_DELAY`.

## Colors
Use the `Color` type and colors defined in `style`. Do not use colors from manim directly.

## Building Animations
Animations used on the live website should be built as `gif`s with medium (`-qm`) quality. The output file
name (`-o [FILENAME]`) should be lowercase with underscores for spaces.
```
%%manim -v CRITICAL --format gif --disable_caching -qm -o boundary_constraints BoundaryConstraintScene
```

## Using Animations
Animations should generally be displayed using the `figure` environment. 
Animations should be displayed in the website by copying them from `animations` into the appropriate folder in `source`.
```
:::{figure} boundary_constraints.gif
:alt: Constraining the boundary
:width: 80%
:align: center
Constraining a boundary line
:::
```
Tutorials with only a handful of animations my place all content in the same tutorial folder. Large tutorials may include
a `media` folder.

# Code
## Writing Animations
Animation helpers and members should be marked with `_`. 
`setup` should be used to set constant data for scenes.
Large animations may choose to abbreviate `self` as `s`.
Scenes should not be passed as arguments to classes without good reason.

## Classes
### Naming
Class members should generally be marked private by prepending an underscore, e.g. `_my_value`. 
Internal class methods should also be marked private by prepending an underscore, e.g. `_internal_func`.

Setters should be prepended with `set`. Note setters should be made chainable by having them
return an instace of themselves.

Getters may be prepended with `get`, but this is optional. Prefer writing a `getter` over making a 
value `public`.

### Chaining
Setters, as well as other methods with no default return value, should generally enable chaining
by returning an instance of themselves (Typed using `Self`).

### Factories
Classes with factory methods should include the methods as static members and name them `make`. 

Do not require calling setter methods between initialization of a class and use of a class method.
For non-trivial classes, prefer to use direct injection and write factories instead of writing 
complex constructors.

## Imports
Avoid polluting namespaces by importing with `*`.
Manim may be imported using `from Manim import *`.
Import user types using `from rc_lib import math_types as T`. Import other custom types directly.

## Types
Classes should be typed using Python type hints. The following rules apply:
* Type the return type of `__init__` methods with `None`.
* Use defined types from `math_types` and elsewhere as appropriate. Avoid using `np.ndarray` directly.
* User defined types may be imported aliased as `T`.
* Union types should be defined using Python 10 `|` syntax, e.g. `str | None` instead of `Optional[str]`.
* Note `Optional` is used for kwargs which are intended to allow explicitly passing the value `None`. This should not be confused
    with not passing the type at all.
* Use `Self` when a method returns an instance of it's own class.
* Type returns using the base class. For example, return an `Animation`, not a `Succession`, and a `VMObject`, not a `VGroup`.

## Spelling
Spellings not recognized by the spellchecker should either corrected or added to the `.vscode` workspace settings using the quick fix menu.

# Website
## Headers
Headers should be written in capital case, e.g. **My Header** instead of **My header**.

## Hyperlinks
Avoid displaying hyperlinks directly in the website; use aliases instead.

## Directives
Use colons (`:::`) instead of backticks (`` ``` ``) to mark directives.

## Admonition Directives
Admonitions are directives which may be used to create special info boxes which
define additional information. 
```
:::{note}
Consider doing X.
:::

:::{warning}
Do Y first to prevent X.
:::
```

Admonitions should be used somewhat sparingly in order to avoid oversaturating users.
Admonition content should be written in complete sentences with proper punctuation. 
`warning` and `danger` admonitions should also generally include a description of the consequence if the information is disregarded.

Below is a detailed breakdown of the different types of admonitions as well as guidance on when to use them:
- `note`: Use `note` to define information which is possibly relevant but not directly related to the task at hand. \
    Example: "You should commit your changes consistently when working on code."
- `warning`: Use `warning` to define information that, when missed, may cause confusion or additional problems. \
    Example: "Make sure you have chocolatey installed first; otherwise, the install may fail."
- `danger`: Use `danger` to define information that, when missed, may cause serious problems which are challenging to fix. \
    Example: "Make sure you have chocolatey installed first; otherwise, the install may become corrupted."
- `important`: Use `important` to define information which is highly relevant but which does not have any significant consequences if missed. Note there is some grey area between `important` and `warning`; use your best judgement. \
    Example: "If you use `--amend` to modify a commit which has already been pushed to the cloud, you should use `git push --force` to avoid a merge conflict on your next push."
- `tip`: Use `tip` instead of `note` when the information is not strictly necessary for basic users. \
    Example: "You can use `--amend` to update your previous commit, and `--no-edit` to avoid having to re-specify the commit message."

The following admonitions should not be used:
- `hint`: `hint` is too similar to `tip` and `note`. 
- `attention`: `attention` is too similar to `warning` and `important`.
- `caution`: `caution` is too similar to `warning`, `danger`, and `important`.
- `error`: `error`'s use case is too niche to justify using it.