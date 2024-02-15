# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import sys
import os

sys.path.append(os.path.abspath("/extensions"))


# -- Project information -----------------------------------------------------

project = "Robot Education"
copyright = "2023, Alex Kempen"
author = "Alex Kempen"

# The full version, including alpha/beta/rc tags
release = "1.0.0"


# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx_rtd_theme",
    # "sphinx.ext.autosectionlabel",
    "sphinx.ext.githubpages",
    "sphinx_copybutton",
    "myst_parser",
    # custom animation extension
    "extensions.animation",
]

myst_enable_extensions = [
    "strikethrough",  # Strikethrough: ~~strike~~
    "amsmath",  # Parse amsmath equations, e.g. \begin{align} 2 = 2 \end{align}
    "dollarmath",  # Parse $2 = 2$ and $$2 = 2$$
    "substitution",  # Enables substituions here and at the top of files
    "colon_fence",  # Enables directives using ::: and md-figure directive
    "attrs_inline",
    "substitution",
    "attrs_block",
    "attrs_inline",
]

# autosectionlabel_prefix_document = True

templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_style"]

html_css_files = ["custom.css"]

myst_substitutions = {
    "coincident": "![coincident](/images/coincident.svg){.inline}",
    "vertical": "![vertical](/images/vertical.svg){.inline}",
    "horizontal": "![horizontal](/images/horizontal.svg){.inline}",
    "parallel": "![parallel](/images/parallel.svg){.inline}",
    "perpendicular": "![perpendicular](/images/perpendicular.svg){.inline}",
    "equal": "![equal](/images/equal.svg){.inline}",
    "midpoint": "![midpoint](/images/midpoint.svg){.inline}",
    "tangent": "![tangent](/images/tangent.svg){.inline}",
    "concentric": "![concentric](/images/concentric.svg){.inline}",
}
