import typing as t
from .markdown import Markdown, MarkdownType, Renderable, dumps


class Bold(Markdown):
    __regex__: str = r"\*\*(.+)\*\*"

    def __init__(self, content: MarkdownType) -> None:
        self.content = content

    def dumps(self, *args: t.Any, **kwargs: t.Any) -> Renderable:
        yield f"**{dumps(self.content)}**"


class Italics(Markdown):
    __regex__: str = r"\*(.+)\*"

    def __init__(self, content: MarkdownType) -> None:
        self.content = content

    def dumps(self, *args: t.Any, **kwargs: t.Any) -> Renderable:
        yield f"*{dumps(self.content)}*"
