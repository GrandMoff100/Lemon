import typing as t

from .markdown import MarkdownType, Renderable, Text


class StyleMixin(Text):
    __ignore__: bool = True

    def __init__(self, content: str) -> None:
        super().__init__(content.strip())

    @property
    def content(self) -> str:
        return t.cast(str, self.elements[0])

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}({self.content!r})"

    def __eq__(self, other: t.Any) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.content == other.content

    @property
    def __children__(self) -> list[Renderable]:
        return [self.content]

    @classmethod
    def loads(cls, _: dict[str, t.Any] | None, content: str) -> MarkdownType:  # type: ignore[override] # pylint: disable=arguments-differ
        return cls(content)

    def dumps(self, *args: t.Any, **kwargs: t.Any) -> str:
        # Prevents circular import!
        from .serialize import dumps  # pylint: disable=import-outside-toplevel

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


class InlineCode(StyleMixin):
    __regex__: str = r"(?:(?<!\\)``(?!`)(.+?)(?<!\\)``)|(?:(?<!\\)`(?!`)\1(?<!\\)`)"

    def dumps(self, *args: t.Any, **kwargs: t.Any) -> str:
        return f"``{super().dumps(*args, **kwargs)}``"
