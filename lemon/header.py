from .markdown import Markdown, MarkdownType, Renderable, render


class Header(Markdown):
    def __init__(self, name: MarkdownType, body: Renderable = ""):
        self.name = name
        self.body = body

    def render(self, *args, depth: int = 0, **kwargs) -> "Renderable":
        yield f"#{'#' * depth} {render(self.name, *args, **kwargs)}"
        yield render(self.body, *args, kwargs, depth=depth + 1)
