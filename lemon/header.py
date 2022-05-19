import typing as t

from .markdown import Markdown, MarkdownType, Renderable


class Header(Markdown):
    __regex__: str = r"\#+\ +(.+)\n((?:.|\n)+)"

    def __init__(self, name: MarkdownType, body: Renderable = "") -> None:
        self.name = name
        self.body = body

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}({self.name!r}, {self.body!r})"

    def __eq__(self, other: t.Any) -> bool:
        if not isinstance(other, Header):
            return False
        return self.name == other.name and self.body == other.body

    def dumps(self, *args: t.Any, depth: int = 0, **kwargs: t.Any) -> str:
        from .serialize import dumps

        body = dumps(self.body, *args, **kwargs, depth=depth + 1)
        return f"#{'#' * depth} {dumps(self.name, *args, **kwargs)}{body}"

    @classmethod
    def loads(cls, ctx: t.Optional[t.Dict[str, t.Any]], name: str, body: str) -> MarkdownType:  # type: ignore[override]
        from .serialize import loads

        return cls(name=name.strip(), body=loads(body))
