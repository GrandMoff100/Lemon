import typing as t


class Markdown:
    pass


MarkdownType = t.Union[Markdown, str]


class Header(Markdown):
    def __init__(self, name: str, body: Markdown, depth: int = 0):
        self.name = name
        self.content = content
        self.depth = depth
