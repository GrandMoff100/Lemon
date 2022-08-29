import typing as t

from .markdown import Markdown, MarkdownType, Renderable
from .serialize import dumps


class Blockquote(Markdown):
    __regex__: str = r">\ *(.*)"

    def __init__(self, body: Renderable) -> None:
        self.body = body
        super().__init__({})

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}({self.body!r})"

    def __eq__(self, other: t.Any) -> bool:
        if not isinstance(other, Blockquote):
            return False
        return self.body == other.body

    def dumps(self, *args: t.Any, depth: int = 0, **kwargs: t.Any) -> str:
        body = dumps(self.body, *args, **kwargs, depth=depth + 1)
        return f"> {body}"

    @classmethod
    def loads(  # type: ignore[override]  # pylint: disable=arguments-differ
        cls,
        _: dict[str, t.Any] | None,
        content: str,
    ) -> MarkdownType:
        return cls(body=content)
