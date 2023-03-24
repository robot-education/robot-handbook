from typing import List
import pathlib

from docutils import nodes
from sphinx.util import docutils, logging
from sphinx import application

logger = logging.getLogger(__name__)


class source(nodes.Inline, nodes.Element):
    """
    A docutils node corresponding to a source html element.
    """

    pass


class SourceTranslator(docutils.SphinxTranslator):
    def visit_source(self, node: source) -> None:
        src_path = (
            pathlib.Path(self.builder.imgpath) / pathlib.Path(node["src"]).parts[-1]
        ).as_posix()

        attributes = {"src": src_path, "type": node["type"]}
        self.body.append(self.emptytag(node, "source", **attributes))

    def depart_source(self, _: source) -> None:
        """Exit the video node."""
        pass


class video(nodes.General, nodes.Element):
    """
    A docutils node corresponding to a video html element.
    """

    pass


class VideoTranslator(docutils.SphinxTranslator):
    def visit_video(self, node: video) -> None:
        # value attributes
        attr: List[str] = [
            '{k} = "v"'.format(k=k, v=node[k])
            for k in [
                "controlslist",
                "crossorigin",
                "height",
                "width",
                "poster",
                "preload",
                "src",
            ]
            if node[k]
        ]

        # boolean attributes
        attr.extend(
            [
                k
                for k in [
                    "autoplay",
                    "autopictureinpicture",
                    "controls",
                    "disablepictureinpicture",
                    "disableremoteplayback",
                    "loop",
                    "playsinline",
                    "muted",
                ]
                if node[k]
            ]
        )
        self.body.append("<video {}>\n".format(" ".join(attr)))

    def depart_video(self, _: video) -> None:
        """Exit the video node."""
        self.body.append("</video>\n")


def visit_node_unsupported(translator: docutils.SphinxTranslator, node: video) -> None:
    """Entry point of the ignored video node."""
    logger.warning("unsupported output format (node skipped)")
    raise nodes.SkipNode


def add_nodes(app: application.Sphinx) -> None:
    """
    Registers nodes with sphinx
    """
    app.add_node(
        video,
        html=(VideoTranslator.visit_video, VideoTranslator.depart_video),
        epub=(visit_node_unsupported, None),
        latex=(visit_node_unsupported, None),
        man=(visit_node_unsupported, None),
        texinfo=(visit_node_unsupported, None),
        text=(visit_node_unsupported, None),
    )

    app.add_node(
        source,
        html=(SourceTranslator.visit_source, SourceTranslator.depart_source),
        epub=(visit_node_unsupported, None),
        latex=(visit_node_unsupported, None),
        man=(visit_node_unsupported, None),
        texinfo=(visit_node_unsupported, None),
        text=(visit_node_unsupported, None),
    )
