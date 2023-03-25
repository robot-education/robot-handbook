from typing import List
import pathlib

from docutils import nodes
from sphinx.util import docutils, logging
from sphinx.writers import html
from sphinx import application

logger = logging.getLogger(__name__)


class source(nodes.Inline, nodes.Element):
    """
    A docutils node corresponding to a source html element.
    """

    pass


class video(nodes.General, nodes.Element):
    """
    A docutils node corresponding to a video html element.
    """

    pass


class VideoTranslator(html.HTMLTranslator, docutils.SphinxTranslator):
    def _get_src_path(self, src: str) -> str:
        return (
            pathlib.Path(self.builder.imgpath) / pathlib.Path(src).parts[-1]
        ).as_posix()

    def visit_source(self, node: source) -> None:
        src_path = self._get_src_path(node["src"])
        attributes = {"src": src_path, "type": node["type"]}
        self.body.append(self.emptytag(node, "source", **attributes))

    def depart_source(self, _: source) -> None:
        """Exit the video node."""
        pass

    def visit_video(self, node: video) -> None:
        if "src" in node:
            node["src"] = self._get_src_path(node["src"])

        attributes: List[str] = [
            '{k} = "{v}"'.format(k=k, v=node[k])
            for k in [
                "controlslist",
                "crossorigin",
                "height",
                "width",
                "poster",
                "preload",
                "src",
            ]
            if k in node
        ]

        # boolean attributes
        attributes.extend(
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
                if k in node
            ]
        )
        self.body.append("<video {}>\n".format(" ".join(attributes)))

    def depart_video(self, _: video) -> None:
        """Exit the video node."""
        self.body.append("</video>\n")


# No args might not be valid here, I haven't checked
def visit_node_unsupported() -> None:
    """Entry point of the ignored video node."""
    logger.warning("unsupported output format (node skipped)")
    raise nodes.SkipNode


unsupported_tuple = (visit_node_unsupported, None)
unsupported_dict = dict(
    [(k, unsupported_tuple) for k in ["epub", "latex", "man", "texinfo", "text"]]
)


def register_video_nodes(app: application.Sphinx) -> None:
    """
    Registers video nodes and the updated translator with sphinx
    """
    app.set_translator("html", VideoTranslator)

    app.add_node(video, **unsupported_dict)
    app.add_node(source, **unsupported_dict)
