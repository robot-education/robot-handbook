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

VIDEO_PARAMETERS: List[str] = [
    "width",
    "autoplay",
    "loop",
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
    path = "design/plate/media/" + src
    # logger.warning(path)

    # if not bool(urlparse(path).netloc):
    env.images.add_file("plate.md", path)

    suffix = Path(src).suffix
    if suffix not in SUPPORTED_MIME_TYPES:
        logger.warning(
            'The provided file type ("{}") is not a supported format. defaulting to ""'.format(
                suffix
            )
        )
    type = SUPPORTED_MIME_TYPES.get(suffix, "")

    return (src, type)


class video_node(nodes.image, nodes.General, nodes.Element):
    """
    Video node combining nodes.General with nodes.Element.
    Named lowercase to match html naming convention.
    """


def size(argument: str):
    return directives.choice(argument, ("standard", "small"))


class Animation(SphinxDirective):
    """Animation directive.
    Wrapper for the html <video> tag embeding all the supported options
    """

    # enable content in the directive
    has_content: bool = True
    # file name
    required_arguments: int = 1
    optional_arguments: int = 0
    option_spec: Dict[str, Any] = {
        "autoplay": directives.flag,
        "loop": directives.flag,
        "size": size,
    }

    def run(self) -> List[video_node]:
        """Return the video node based on the set options."""
        self.assert_has_content()
        # env: BuildEnvironment = self.env

        # width: str = self._parse_size()
        size: str = self.options["size"]
        width = SIZE_LOOKUP["standard" if size is None else size]

        reference = directives.uri(self.arguments[0])

        node = video_node(
            rawsource=self.block_text,
            uri=reference,
            width=width,
            autoplay="autoplay" in self.options,
            loop="loop" in self.options,
        )
        # logger.info(node)
        return [node]


def visit_video_node_html(translator: SphinxTranslator, node: video_node) -> None:
    """Entry point of the html video node."""
    # start the video block
    attribute_string: str = '{key}="{value}"'
    attr: List[str] = [
        attribute_string.format(key=k, value=node[k])
        for k in ["width", "autoplay", "loop"]
        if node[k]
    ]
    attr.extend(
        [attribute_string.format(key=k, value=v) for v, k in enumerate(FIXED_OPTIONS)]
    )

    html: str = "<video {}>\n".format(" ".join(attr))
    html += '<source src="{}" type="video/mp4">\n'.format(
        node["uri"]
    )  # build the sources

    # add the alternative message
    # html += node["content"]
    html += "</video>\n"
    translator.body.append(html)


def visit_video_node_unsupported(_: SphinxTranslator, node: video_node) -> None:
    """Entry point of the ignored video node."""
    logger.warning("video {}: unsupported output format (node skipped)".format(".mp4"))
    raise nodes.SkipNode


def setup(app: Sphinx) -> Dict[str, bool]:
    """Add video node and parameters to the Sphinx builder."""
    app.add_node(
        video_node,
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
