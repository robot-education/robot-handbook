"""
A sphinx extension designed to work with the build script to automatically insert programs into the build directory.

Supports .mp4 videos compiled by the build script.
"""

import copy
from typing import Any, Dict, List, cast
from pathlib import Path

from sphinx import application
from sphinx.util import docutils as sphinx_docutils, typing, logging

from docutils.parsers.rst import directives as docutils_directives
from docutils import nodes

# from myst_parser.parsers import directives as myst_directives
from myst_parser import mocking as myst_mocking

from video_extension import local_nodes

logger = logging.getLogger(__name__)

SIZE_LOOKUP: Dict[str, str] = {"small": "60%", "standard": "80%"}
"Maps size options to the width"


def size(argument: str):
    return docutils_directives.choice(argument, ("standard", "small"))


class Animation(sphinx_docutils.SphinxDirective):
    """Animation directive.
    Wrapper for the html <video> tag embeding all the supported options
    """

    # enable content in the directive
    has_content: bool = True
    final_argument_whitespace: bool = True

    # file name
    required_arguments: int = 1
    optional_arguments: int = 0
    option_spec: typing.OptionSpec = {
        "autoplay": docutils_directives.flag,
        "size": size,
    }

    def run(self) -> List[nodes.Node]:
        uri = self._parse_uri()

        figure_node = nodes.figure(
            rawsource=self.block_text,
            align="center",  # may also be left or right
        )

        video_node = local_nodes.video(
            # add entire directive for error handling
            rawsource=self.block_text,
            src=uri,
            width=self._parse_width(),
            autoplay=("autoplay" in self.options),
            loop=("autoplay" in self.options),
            controls=True,
            playsinline=True,
            muted=True,
            disablepictureinpicture=True,
        )

        # optional - use source nodes to support multiple sources
        # source_node = local_nodes.source(
        #     rawsource=self.arguments[0], src=uri, type="video/mp4"
        # )
        # video_node += source_node

        # Add caption
        figure_node += video_node
        return [self._add_caption(figure_node)]

    def _parse_alt(self, caption: str) -> str:
        return self.options["alt"] if "alt" in self.options else caption

    def _parse_width(self) -> str:
        return SIZE_LOOKUP[
            self.options["size"] if "size" in self.options else "standard"
        ]

    def _parse_uri(self) -> str:
        path = Path(self.arguments[0])
        if len(path.parts) == 1:
            path = "media" / path
        else:
            logger.warning('Animations may omit the "media" folder in their path')
        return docutils_directives.uri(path.as_posix())

    def _add_caption(self, figure_node: nodes.figure) -> nodes.Node:
        """
        Adds the caption to the animation.
        Copied from docutil's figure directive class:
        https://github.com/docutils/docutils/blob/master/docutils/docutils/parsers/rst/directives/images.py
        """
        self.assert_has_content()

        state = cast(myst_mocking.MockState, self.state)

        node = nodes.Element()
        state.nested_parse(self.content, self.content_offset, node)

        caption_para = node.children[0]
        if not isinstance(caption_para, nodes.paragraph):
            return self.figure_error(
                "content should be followed by single paragraph caption (not found)"
            )

        caption_node = nodes.caption(caption_para.rawsource, "", *caption_para.children)  # type: ignore
        caption_node.source = caption_para.source
        caption_node.line = caption_para.line

        figure_node += caption_node
        self.set_source_info(figure_node)

        return figure_node

    def figure_error(self, message: str) -> nodes.Node:
        """A warning for reporting an invalid figure."""
        error = self.state_machine.reporter.error(
            message,
            nodes.literal_block(self.block_text, self.block_text),
            line=self.lineno,
        )
        return error


def setup(app: application.Sphinx) -> Dict[str, bool]:
    """Add video node and parameters to the Sphinx builder."""
    local_nodes.register_video_nodes(app)

    app.add_directive("animation", Animation)

    # app.builder.supported_image_types = [
    #     "image/svg+xml",
    #     "image/png",
    #     "image/gif",
    #     "video/mp4",
    # ]

    return {
        "parallel_read_safe": True,
        "parallel_read_write": True,
    }
