"""
A sphinx extension designed to work with the build script to automatically insert programs into the build directory.

Supports .mp4 videos compiled by the build script.
"""

"""
Videos have the following settings:
autoplay: optional, true for gif like content - defaults to false
loop: optional, true for gif like content - defaults to false
width: set based on SIZE, defaults to standard (80%)
controls: true
muted: true
playsinline: true
preload: metadata
"""

from pathlib import Path
from typing import Any, Dict, List, Tuple
from urllib.parse import urlparse

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.application import Sphinx
from sphinx.environment import BuildEnvironment
from sphinx.util import logging
from sphinx.util.docutils import SphinxDirective, SphinxTranslator

logger = logging.getLogger(__name__)

SIZE_LOOKUP: Dict[str, str] = {"small": "60%", "standard": "80%"}
"Maps size options to the width"

SUPPORTED_MIME_TYPES: Dict[str, str] = {".mp4": "video/mp4"}
"Supported mime types of the link tag"

SUPPORTED_OPTIONS: List[str] = [
    "size",
    "autoplay",
    "loop"
    # "preload",
    # "controls",
    # "height",
    # "muted",
    # "poster",
    # "preload",
    # "width",
]
"List of the supported options attributes"

FIXED_OPTIONS: Dict[str, Any] = {
    "muted": True,
    "preload": "auto",
    "controls": True,
}


def get_video(src: str, env: BuildEnvironment) -> Tuple[str, str]:
    """
    Return video and suffix.
    Load the video to the static directory if necessary and process the suffix. Raise a warning if not supported but do not stop the computation.
    Args:
        src: The source of the video file (can be local or url)
        env: the build environment
    Returns:
        the src file, the extention suffix
    """
    if not bool(urlparse(src).netloc):
        env.images.add_file("", src)

    suffix = Path(src).suffix
    if suffix not in SUPPORTED_MIME_TYPES:
        logger.warning(
            'The provided file type ("{}") is not a supported format. defaulting to ""'.format(
                suffix
            )
        )
    type = SUPPORTED_MIME_TYPES.get(suffix, "")

    return (src, type)


class VideoNode(nodes.General, nodes.Element):
    """
    Video node combining nodes.General with nodes.Element.
    Named lowercase to match html naming convention.
    """


class Animation(SphinxDirective):
    """Animation directive.
    Wrapper for the html <video> tag embeding all the supported options
    """

    # enable content in the directive
    has_content: bool = True
    # file name
    required_arguments: int = 1
    # optional_arguments: int = 1
    option_spec: Dict[str, Any] = {
        "autoplay": directives.flag,
        "loop": directives.flag,
        "size": directives.unchanged,
    }

    def _parse_size(self) -> str:
        size: str = self.options.get("size", "")
        if SIZE_LOOKUP[size] != None:
            return SIZE_LOOKUP[size]

        logger.warning(
            'The provided size ({}) is ignored as it is not "standard" or "small"'.format(
                size
            )
        )
        return SIZE_LOOKUP["standard"]

    def run(self) -> List[VideoNode]:
        """Return the video node based on the set options."""
        env: BuildEnvironment = self.env

        width: str = self._parse_size()

        if self.content == "":
            logger.warning("Expected text to use as a caption")

        return [
            VideoNode(
                primary_src=get_video(self.arguments[0], env),
                content=self.content,
                width=width,
                autoplay="autoplay" in self.options,
                loop="loop" in self.options,
            )
        ]


def visit_video_node_html(translator: SphinxTranslator, node: VideoNode) -> None:
    """Entry point of the html video node."""
    # start the video block
    attr: List[str] = [
        '{k}="{node[k]}"'.format(k=k) for k in SUPPORTED_OPTIONS if node[k]
    ]
    html: str = "<video {}>".format(" ".join(attr))

    # build the sources
    html_source = "<source src='{}' type='{}'>"

    html += html_source.format(*node["primary_src"])

    # add the alternative message
    html += node["alt"]

    translator.body.append(html)

    translator.body.append("</video>")


# def depart_video_node_html(translator: SphinxTranslator, node: VideoNode) -> None:
#     """Exit of the html video node."""


def visit_video_node_unsupported(translator: SphinxTranslator, node: VideoNode) -> None:
    """Entry point of the ignored video node."""
    logger.warning(
        "video {}: unsupported output format (node skipped)".format(node["primary_src"])
    )
    raise nodes.SkipNode


def setup(app: Sphinx) -> Dict[str, bool]:
    """Add video node and parameters to the Sphinx builder."""
    app.add_node(
        VideoNode,
        html=(visit_video_node_html, None),
        epub=(visit_video_node_unsupported, None),
        latex=(visit_video_node_unsupported, None),
        man=(visit_video_node_unsupported, None),
        texinfo=(visit_video_node_unsupported, None),
        text=(visit_video_node_unsupported, None),
    )
    app.add_directive("animation", Animation)

    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
