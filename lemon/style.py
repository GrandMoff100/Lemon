import typing as t

from .markdown import Markdown, MarkdownType, Renderable, dumps


class StyleMixin(Markdown):
    __ignore__: bool = True

    def __init__(self, content: str) -> None:
        self.content = content.strip()

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}({self.content!r})"

    @classmethod
    def loads(cls, ctx: t.Dict[str, t.Any], content: str) -> MarkdownType:  # type: ignore[override]
        return cls(content)

    def dumps(self, *args, **kwargs) -> str:
        kwargs["inline"] = True
        return dumps(self.content, *args, **kwargs).strip()


class Bold(StyleMixin):
    __regex__: str = r"(?<!\\)\*\*(.+?)(?<!\\)\*\*"

    def dumps(self, *args: t.Any, **kwargs: t.Any) -> str:
        return f"**{super().dumps(*args, **kwargs)}**"


class Italics(StyleMixin):
    __regex__: str = r"(?<!\\)\*(.+?)(?<!\\)\*"

    def dumps(self, *args: t.Any, **kwargs: t.Any) -> str:
        return f"*{super().dumps(*args, **kwargs)}*"


class Strikethrough(StyleMixin):
    __regex__: str = r"(?<!\\)~~(.+?)(?<!\\)~~"

    def dumps(self, *args: t.Any, **kwargs: t.Any) -> str:
        return f"~~{super().dumps(*args, **kwargs)}~~"
