from .markdown import Markdown, MarkdownType, Renderable, render


class Bold(Markdown):
    def __init__(self, content: MarkdownType) -> None:
        self.content = content

    def render(self, *args, **kwargs):
        yield f"**{render(self.content)}**"


class Italics(Markdown):
    def __init__(self, content: MarkdownType) -> None:
        self.content = content

    def render(self, *args, **kwargs):
        yield f"*{render(self.content)}*"
