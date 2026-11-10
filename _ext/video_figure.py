"""Render ``{figure}`` directives that point at a video file as HTML5 video.

Sphinx only knows how to embed images. A ``{figure}`` whose target is an
``.mp4``/``.webm``/``.ogv`` file would be written as ``<img src="...mp4">``: the
video would not play and the file would not even be copied into the build.

This local extension walks the doctree before the HTML writer runs and replaces
such image nodes with a ``<video>`` element. The surrounding ``figure`` node is
left untouched, so caption, "Fig. X.Y" numbering, figure id and cross-references
keep working. ``build-finished`` copies the video files into ``_videos/`` next to
the generated pages, mirroring what Sphinx does for images in ``_images/``.

Usage in Markdown::

    ```{figure} ../assets/annotation/example.mp4
    ---
    width: 100%
    alt: Beschreibung der Animation.
    ---
    Bildunterschrift.
    ```

Videos autoplay muted in a loop (like the GIFs they replace) and are rendered
without native controls; _static/video-figure.js makes a click (or Space/Enter)
toggle play/pause and pauses videos that are scrolled out of view.
"""

from __future__ import annotations

import hashlib
import html
import shutil
from pathlib import Path
from typing import Any

from docutils import nodes
from sphinx.transforms import SphinxTransform
from sphinx.util import logging
from sphinx.util.osutil import relative_uri

LOGGER = logging.getLogger(__name__)

VIDEO_SUFFIXES = (".mp4", ".webm", ".ogv")
VIDEO_DIR = "_videos"


def _is_video(uri: str) -> bool:
    return uri.lower().endswith(VIDEO_SUFFIXES)


def _css_size(value: str) -> str:
    """Return a CSS length for a docutils ``width``/``height`` value."""
    value = value.strip()
    return value if value.endswith(("%", "px", "em", "rem", "vw", "vh")) else f"{value}px"


class VideoFigureTransform(SphinxTransform):
    """Replace image nodes that point at a video file with a ``<video>`` tag."""

    # Run before the HTML writer resolves image URIs (default 880).
    default_priority = 400

    def apply(self, **_kwargs: Any) -> None:
        if self.app.builder.format != "html":
            return

        for node in list(self.document.findall(nodes.image)):
            uri = node["uri"]
            if _is_video(uri):
                self._replace_with_video(node, uri)

    def _replace_with_video(self, node: nodes.image, uri: str) -> None:
        target = self._register_video(uri)
        src = relative_uri(self.app.builder.get_target_uri(self.env.docname), target)

        attributes = [
            f'src="{src}"',
            "autoplay",
            "loop",
            "muted",
            "playsinline",
        ]
        alt = node.get("alt")
        if alt:
            attributes.append(f'aria-label="{html.escape(alt, quote=True)}"')
        if node.get("width"):
            attributes.append(f'style="width: {_css_size(node["width"])};"')
        if node.get("height"):
            attributes.append(f'height="{_css_size(node["height"])}"')

        video = nodes.raw(
            "", f'<video class="book-video" {" ".join(attributes)}></video>', format="html"
        )

        # Mark the enclosing figure so the stylesheet can add a video icon to
        # the caption (see _static/quadriga.css).
        figure = node.parent
        while figure is not None and not isinstance(figure, nodes.figure):
            figure = figure.parent
        if isinstance(figure, nodes.figure):
            figure["classes"].append("figure-video")

        # ``{figure}`` wraps the image in a link when scaled-image links are
        # enabled; drop that wrapper so the video is not a clickable <a>.
        parent = node.parent
        if isinstance(parent, nodes.reference) and len(parent) == 1:
            parent.replace_self(video)
        else:
            node.replace_self(video)

    def _register_video(self, uri: str) -> str:
        """Return the output-relative path the video is copied to."""
        videos: dict[str, str] = getattr(self.env, "video_files", None) or {}
        setattr(self.env, "video_files", videos)  # noqa: B010 - not a real attribute

        target = videos.get(uri)
        if target is None:
            name = uri.rsplit("/", 1)[-1]
            target = f"{VIDEO_DIR}/{name}"
            if target in videos.values():
                # Two different videos share a file name: keep them apart.
                digest = hashlib.sha256(uri.encode("utf-8")).hexdigest()[:8]
                target = f"{VIDEO_DIR}/{digest}-{name}"
            videos[uri] = target
        return target


def copy_video_files(app: Any, exception: Exception | None) -> None:
    """Copy registered videos into the build output."""
    if exception is not None or app.builder.format != "html":
        return

    srcdir = Path(app.builder.srcdir)
    outdir = Path(app.builder.outdir)
    videos: dict[str, str] = getattr(app.env, "video_files", {})

    for uri, target in videos.items():
        source = srcdir / uri
        if not source.is_file():
            LOGGER.warning("video file not found: %s", source)
            continue
        destination = outdir / target
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)


def setup(app: Any) -> dict[str, Any]:
    app.add_post_transform(VideoFigureTransform)
    app.connect("build-finished", copy_video_files)
    return {"version": "1.0", "parallel_read_safe": True, "parallel_write_safe": True}
