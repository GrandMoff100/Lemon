import typing as t
from .markdown import Markdown, MarkdownType, Renderable, render


class Header(Markdown):
    _regex = r"#+(.+)\n"

    def __init__(self, name: MarkdownType, body: Renderable = "") -> None:
        self.name = name
        self.body = body

    def render(self, *args: t.Any, depth: int = 0, **kwargs: t.Any) -> "Renderable":
        yield f"#{'#' * depth} {render(self.name, *args, **kwargs)}"
        yield render(self.body, *args, kwargs, depth=depth + 1)
