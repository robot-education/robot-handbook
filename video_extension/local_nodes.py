"""
Local nodes which may be used to create videos.
Useful links:


rst directive writing documentation:
https://docutils.sourceforge.io/docs/howto/rst-directives.html

image directive source code:
https://github.com/docutils/docutils/blob/master/docutils/docutils/parsers/rst/directives/images.py
"""


from typing import Any, List
import os

from docutils import nodes
from sphinx.util import docutils, logging
from sphinx.writers import html as html_writers
from sphinx import application, transforms
from sphinx.builders import html as html_builders

# from sphinx.environment.adapters import asset

# logger = logging.getLogger(__name__)


class source(nodes.Inline, nodes.Element):
    """
    A docutils node corresponding to a source html element.
    """

    pass


class video(nodes.General, nodes.TextElement):
    """
    A docutils node corresponding to a video html element.
    """

    pass


class VideoTransform(transforms.SphinxTransform):
    def apply(self, **kwargs: Any) -> None:
        for node in list(self.document.findall(video)) + list(
            self.document.findall(source)
        ):
            self.handle(node)

    def handle(self, node: video | source) -> None:
        file_name = Path(node["src"])
        dest_path = os.path.join(self.imagedir, file_name)
        abs_src_path = os.path.join(self.app.srcdir, src_path)
        if self.convert(abs_src_path, dest_path):
            if "*" in node["candidates"]:
                node["candidates"]["*"] = dest_path
            else:
                node["candidates"][_to] = dest_path
            node["src"] = dest_path

            self.env.original_image_uri[dest_path] = src_path
            self.env.images.add_file(self.env.docname, dest_path)


class VideoBuilder(html_builders.StandaloneHTMLBuilder):
    def post_process_images(self, doctree: nodes.Node) -> None:
        super().post_process_images(doctree)
        # adapter = asset.ImageAdapter(self.env)
        # for node in list(doctree.findall(video)) + list(doctree.findall(source)):
        #     candidate = node["candidates"]["video/mp4"]
        #     node["src"] = candidate
        #     self.images[candidate] = self.env.images[candidate][1]

        # """Pick the best candidate for all image URIs."""
        # images = ImageAdapter(self.env)
        # for node in doctree.findall(nodes.image):
        #     if '?' in node['candidates']:
        #         # don't rewrite nonlocal image URIs
        #         continue
        #     if '*' not in node['candidates']:
        #         for imgtype in self.supported_image_types:
        #             candidate = node['candidates'].get(imgtype, None)
        #             if candidate:
        #                 break
        #         else:
        #             mimetypes = sorted(node['candidates'])
        #             image_uri = images.get_original_image_uri(node['uri'])
        #             if mimetypes:
        #                 logger.warning(__('a suitable image for %s builder not found: '
        #                                   '%s (%s)'),
        #                                self.name, mimetypes, image_uri, location=node)
        #             else:
        #                 logger.warning(__('a suitable image for %s builder not found: %s'),
        #                                self.name, image_uri, location=node)
        #             continue
        #         node['uri'] = candidate
        #     else:
        #         candidate = node['uri']
        #     if candidate not in self.env.images:
        #         # non-existing URI; let it alone
        #         continue
        #     self.images[candidate] = self.env.images[candidate][1]


class VideoTranslator(html_writers.HTMLTranslator, docutils.SphinxTranslator):
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
        attributes: List[str] = [
            '{k} = "{v}"'.format(k=k, v=node[k])
            for k in [
                "controlslist",
                "crossorigin",
                "height",
                "width",
                "poster",
                "preload",
            ]
            if k in node
        ]

        if "src" in node:
            uri = self._get_src_path(node["src"])
            attributes.append('src = "{}"'.format(uri))

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

    # def visit_reference(self, node):
    #     if isinstance(node.children[0], video) or isinstance(node.children[0], source):
    #         attributes = {"class": "reference image-reference"}
    #         if "refuri" in node:
    #             attributes["href"] = self._get_src_path(node["refuri"])
    #             attributes["class"] += " external"
    #         else:
    #             assert (
    #                 "refid" in node
    #             ), 'References must have "refuri" or "refid" attribute.'
    #             attributes["href"] = "#" + node["refid"]
    #         self.body.append(self.starttag(node, "a", "", **attributes))
    #     else:
    #         super().visit_reference(node)

    # Don't override depart_reference


# No args might not be valid here, I haven't checked
def visit_node_unsupported(
    translator: docutils.SphinxTranslator, node: nodes.Node
) -> None:
    raise nodes.SkipNode


unsupported_tuple = (visit_node_unsupported, None)
unsupported_dict = dict(
    [(k, unsupported_tuple) for k in ["epub", "latex", "man", "texinfo", "text"]]
)


def register_video_nodes(app: application.Sphinx) -> None:
    """
    Registers video nodes and the updated translator with sphinx
    """
    app.add_builder(VideoBuilder, override=True)
    app.set_translator("html", VideoTranslator)

    app.add_node(video, **unsupported_dict)
    app.add_node(source, **unsupported_dict)
