import typing as t

from .markdown import Markdown, MarkdownType, Renderable, dumps
from .parse import loads


class Header(Markdown):
    __regex__: str = r"\#+\ +(.+)\n((?:.|\n)+)"

    def __init__(self, name: MarkdownType, body: Renderable = "") -> None:
        self.name = name
        self.body = body

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}({self.name!r}, {self.body!r})"

    def dumps(self, *args: t.Any, depth: int = 0, **kwargs: t.Any) -> str:
        from .serialize import dumps

        body = dumps(self.body, *args, **kwargs, depth=depth + 1)
        return f"#{'#' * depth} {dumps(self.name, *args, **kwargs)}{body}"

    @classmethod
    def loads(cls, ctx: t.Optional[t.Dict[str, t.Any]], name: str, body: str) -> MarkdownType:  # type: ignore[override]
        from .serialize import loads

        return cls(name=name.strip(), body=loads(body))
