import typing as t

from .markdown import Markdown, MarkdownType, Renderable, dumps
from .parse import loads


class Header(Markdown):
    __regex__: str = r"#+(?P<name>.+)\n(?P<body>(.|\n)+)"

    def __init__(self, name: MarkdownType, body: Renderable = "") -> None:
        self.name = name
        self.body = body

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}({self.name!r}, {self.body!r})"

    def dumps(self, *args: t.Any, depth: int = 0, **kwargs: t.Any) -> "Renderable":
        yield f"#{'#' * depth} {dumps(self.name, *args, **kwargs)}"
        yield dumps(self.body, *args, kwargs, depth=depth + 1)

    @staticmethod
    def loads(name: str, body: str) -> Renderable:  # type: ignore[override]
        return Header(name=name.strip(), body=loads(body))
