"""
A sphinx extension designed to work with the build script to automatically insert programs into the build directory.

Supports .mp4 videos compiled by the build script.
"""

from typing import Dict, List
from pathlib import Path

from sphinx import application
from sphinx.util import docutils, typing

from docutils.parsers.rst import directives
from docutils import nodes

from video_extension import local_nodes

SIZE_LOOKUP: Dict[str, str] = {"small": "60%", "standard": "80%"}
"Maps size options to the width"


def size(argument: str):
    return directives.choice(argument, ("standard", "small"))


class Animation(docutils.SphinxDirective):
    """Animation directive.
    Wrapper for the html <video> tag embeding all the supported options
    """

    # enable content in the directive
    has_content: bool = True

    # file name
    required_arguments: int = 1
    optional_arguments: int = 0
    option_spec: typing.OptionSpec = {
        "autoplay": directives.flag,
        "size": size,
    }

    def run(self) -> List[nodes.Node]:
        uri = self._parse_uri()
        caption = self._parse_caption()

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

        # ref_node = nodes.reference(refuri=uri)
        # ref_node += video_node
        figure_node += video_node  # ref_node

        # optional - use source nodes to support multiple sources
        # source_node = local_nodes.source(
        #     rawsource=self.arguments[0], src=uri, type="video/mp4"
        # )
        # video_node += source_node

        # Add caption
        figure_node += nodes.caption(rawsource=self.block_text, text=caption)

        return [figure_node]

    def _parse_alt(self, caption: str) -> str:
        return self.options["alt"] if "alt" in self.options else caption

    def _parse_caption(self) -> str:
        self.assert_has_content()
        return "".join(self.content)

    def _parse_width(self) -> str:
        return SIZE_LOOKUP[
            self.options["size"] if "size" in self.options else "standard"
        ]

    def _parse_uri(self) -> str:
        path = Path(self.arguments[0])
        if len(path.parts) == 1:
            path = "media" / path
        else:
            self.warning('Animations may omit the "media" folder in their path')
        return directives.uri(path.as_posix())


def setup(app: application.Sphinx) -> Dict[str, bool]:
    """Add video node and parameters to the Sphinx builder."""
    local_nodes.register_video_nodes(app)
    app.add_directive("animation", Animation)

    return {
        "parallel_read_safe": False,  # sphinx docs suggest we need to actually handle this
    }
