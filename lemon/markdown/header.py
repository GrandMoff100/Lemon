import typing as t

from .markdown import Markdown, MarkdownType, Renderable


class Header(Markdown):
    __regex__: str = r"(?m)^(\#+)\ +(.+)$"

    def __init__(
        self,
        name: MarkdownType,
        level: int = 1,
    ) -> None:
        self.name = name
        self.level = level
        super().__init__({})

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}({self.name!r}, level={self.level!r})"

    def __eq__(self, other: t.Any) -> bool:
        if not isinstance(other, Header):
            return False
        return self.name == other.name and self.level == other.level

    def __hash__(self) -> int:
        return hash(self.dumps())

    @property
    def children(self) -> list[Renderable]:
        return [self.name]

    def dumps(self, *args: t.Any, **kwargs: t.Any) -> str:
        from ..serialize import dumps  # pylint: disable=import-outside-toplevel

        return f"{'#' * self.level} {dumps(self.name, *args, **kwargs)}\n"

    @classmethod
    def loads(  # type: ignore[override]  # pylint: disable=arguments-differ
        cls,
        depth: str,
        name: str,
    ) -> MarkdownType:
        return cls(name=name.strip(), level=len(depth))
