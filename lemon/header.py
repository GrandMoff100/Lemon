import typing as t

from .markdown import Markdown, MarkdownType, Renderable


class Header(Markdown):
    __regex__: str = r"(\#+)\ *(.+)\n"

    def __init__(
        self,
        name: MarkdownType,
        depth: int = 1,
    ) -> None:
        self.name = name
        self.depth = depth
        super().__init__({})

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}({self.name!r}, depth={self.depth!r})"

    def __eq__(self, other: t.Any) -> bool:
        if not isinstance(other, Header):
            return False
        return self.name == other.name and self.depth == other.depth

    @property
    def __children__(self) -> t.List[Renderable]:
        return [self.name]

    def dumps(self, *args: t.Any, **kwargs: t.Any) -> str:
        from .serialize import dumps  # pylint: disable=import-outside-toplevel

        name = dumps(self.name, *args, **kwargs).strip()
        return f"{'#' * self.depth} {name}\n"

    @classmethod
    def loads(  # type: ignore[override]  # pylint: disable=arguments-differ
        cls,
        _: t.Optional[t.Dict[str, t.Any]],
        depth: str,
        name: str,
    ) -> MarkdownType:
        return cls(name=name.strip(), depth=len(depth))
