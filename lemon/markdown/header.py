import typing as t

from .markdown import Markdown, MarkdownType, Renderable


class Header(Markdown):
    __regex__: str = r"\#+\ +(.+)\n((?:.|\n)+)"

    def __init__(
        self,
        name: MarkdownType,
        body: Renderable = "",
    ) -> None:
        self.name = name
        self.body = body
        super().__init__({})

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}({self.name!r}, {self.body!r})"

    def __eq__(self, other: t.Any) -> bool:
        if not isinstance(other, Header):
            return False
        return self.name == other.name and self.body == other.body

    @property
    def __children__(self) -> list[Renderable]:
        return [self.body]

    def dumps(self, *args: t.Any, depth: int = 0, **kwargs: t.Any) -> str:
        from .serialize import dumps  # pylint: disable=import-outside-toplevel

        body = dumps(self.body, *args, **kwargs, depth=depth + 1)
        return f"#{'#' * depth} {dumps(self.name, *args, **kwargs)}{body}"

    @classmethod
    def loads(  # type: ignore[override]  # pylint: disable=arguments-differ
        cls,
        _: dict[str, t.Any] | None,
        name: str,
        body: str,
    ) -> MarkdownType:
        # Prevents a circular import!
        from .serialize import loads  # pylint: disable=import-outside-toplevel

        return cls(name=name.strip(), body=loads(body))
