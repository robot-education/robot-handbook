# Style

This document describes the style guide for the website.

## Headers
Headers should be written in capital case, e.g. **My Header** instead of **My header**.
Top level headers should be underlined with equals signs.

## Hyperlinks
Avoid displaying hyperlinks directly in the website.

## Admonition Directives
Admonitions are directives which may be used to create special info boxes which
define additional information. 
```
.. note::
    Consider doing X.

.. warning::
    Do Y first to prevent X.
```

Admonitions should be used somewhat sparingly in order to avoid oversaturating users.
Admonition content should be written in complete sentences with proper punctuation. 
`warning` and `danger` admonitions should also generally include a description of the consequence if the information is disregarded.

Below is a detailed breakdown of the different types of admonitions as well as guidance on when to use them:
- `note`: Use `note` to define information which is possibly relevant but not directly related to the task at hand. 
    Example: "You should commit your changes consistently when working on code."
- `warning`: Use `warning` to define information that, when missed, may cause confusion or additional problems.
    Example: "Make sure you have chocolatey installed first; otherwise, the install may fail."
- `danger`: Use `danger` to define information that, when missed, may cause serious problems which are challenging to fix.
    Example: "Make sure you have chocolatey installed first; otherwise, the install may become corrupted."
- `important`: Use `important` to define information which is highly relevant but which does not have any significant consequences if missed. Note there is some grey area between `important` and `warning`; use your best judgement.
    Example: "If you use `--amend` to modify a commit which has already been pushed to the cloud, you should use `git push --force` to avoid a merge conflict on your next push."
- `tip`: Use `tip` instead of `note` when the information is not strictly necessary for basic users.
    Example: "You can use `--amend` to update your previous commit, and `--no-edit` to avoid having to re-specify the commit message."

The following admonitions should not be used:
- `hint`: `hint` is too similar to `tip` and `note`. 
- `attention`: `attention` is too similar to `warning` and `important`.
- `caution`: `caution` is too similar to `warning`, `danger`, and `important`.
- `error`: `error`'s use case is to niche to justify using it anywhere.