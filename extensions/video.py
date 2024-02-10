"""
Local nodes which may be used to create videos.

Useful links:
rst directive writing documentation:
https://docutils.sourceforge.io/docs/howto/rst-directives.html

image directive source code:
https://github.com/docutils/docutils/blob/master/docutils/docutils/parsers/rst/directives/images.py
"""

from typing import List

import pathlib

from docutils import nodes
from sphinx.util import docutils
from sphinx.writers import html as html_writers
from sphinx import application, environment
from sphinx.builders import html as html_builders
from sphinx.environment import collectors


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


"""
The build process for images is as follows:
1. A collector runs and does some image stuff. This adds images to the environment and fills in candidates, which
    enables transforms later on.

The sphinx image collector is here:
https://github.com/sphinx-doc/sphinx/blob/ff852bc7c31f48e66100e4647749fc199d92ca79/sphinx/environment/collectors/asset.py

2. Image converters change files from one type to another. 
    They do this using a combination of candidates and updates to the environment and uri to correct the paths.
    We skip this step since we don't worry about changing one video to another.
3. Images are moved from the environment to their specific folders by the appropriate builders. Note this process
    is different for each builder.
    The builder also updates uris to be in-place relative to the correct target folder.
    We update the builder to implement this logic. However, this logic currently targets all https:// links, which 
    is possibly a problem.
"""


class VideoCollector(collectors.EnvironmentCollector):
    def clear_doc(
        self, app: application.Sphinx, env: environment.BuildEnvironment, docname: str
    ) -> None:
        env.images.purge_doc(docname)

    def merge_other(
        self,
        app: application.Sphinx,
        env: environment.BuildEnvironment,
        docnames: set[str],
        other: environment.BuildEnvironment,
    ) -> None:
        env.images.merge_other(docnames, other.images)

    def process_doc(self, app: application.Sphinx, doctree: nodes.document) -> None:
        for node in list(doctree.findall(video)) + list(doctree.findall(source)):
            docname = app.env.docname
            image_uri, _ = app.env.relfn2path(node["src"], docname)
            node["src"] = image_uri
            app.env.dependencies[docname].add(image_uri)
            app.env.images.add_file(docname, image_uri)


class VideoBuilder(html_builders.StandaloneHTMLBuilder):
    def post_process_images(self, doctree: nodes.Node) -> None:
        super().post_process_images(doctree)
        for node in list(doctree.findall(video)) + list(doctree.findall(source)):
            self.images[node["src"]] = self.env.images[node["src"]][1]


class VideoTranslator(html_writers.HTMLTranslator, docutils.SphinxTranslator):
    def _get_src_path(self, src: str) -> str:
        return str(pathlib.PurePath(self.builder.imgpath) / pathlib.PurePath(src).name)

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

        # key value attributes
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
                if k in node and node[k]  # value is truthy
            ]
        )
        self.body.append("<video {}>\n".format(" ".join(attributes)))

    def depart_video(self, _: video) -> None:
        """Exit the video node."""
        self.body.append("</video>\n")


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
    app.add_env_collector(VideoCollector)
    app.add_builder(VideoBuilder, override=True)
    app.set_translator("html", VideoTranslator)

    app.add_node(video, **unsupported_dict)  # type: ignore
    app.add_node(source, **unsupported_dict)  # type: ignore
