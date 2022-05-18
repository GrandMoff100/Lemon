import re
import typing as t
from collections import abc


class Markdown:
    __regex__: str = r"(?P<content>.+)"
    __meta_regex__: str = r"(?:<!--(?P<meta>{.+})-->\n)?"
    __precedence__: t.Tuple[str, ...] = (
        "lemon.header.Header",
        "lemon.tables.Table",
        "lemon.style.Bold",
        "lemon.style.Italics",
        "lemon.markdown.Markdown",
    )

    def __init__(self, *elements: "Renderable") -> None:
        self.elements = elements

    def __repr__(self) -> str:
        if hasattr(self, "elements"):
            return f"{self.__class__.__qualname__}(*{self.elements!r})"
        return f"{self.__class__.__qualname__}()"

    def dumps(self, *args: t.Any, **kwargs: t.Any) -> "Renderable":
        yield " ".join([dumps(element, *args, **kwargs) for element in self.elements])

    @classmethod
    def loads(cls, content: str) -> "Renderable":
        yield cls(content)

    @classmethod
    def _classes(cls) -> t.List[t.Type[Markdown]]:
        return cls.__subclasses__() + [cls]


MarkdownType = t.Union[Markdown, str]
Renderable = t.Union[MarkdownType, t.Iterable[MarkdownType]]


def dumps(content: Renderable, *args: t.Any, **kwargs: t.Any) -> str:
    if isinstance(content, Markdown):
        return dumps(content.dumps(*args, **kwargs), *args, **kwargs)
    if isinstance(content, str):
        return content
    if isinstance(content, abc.Iterable):
        return "\n\n".join([dumps(item, *args, **kwargs) for item in content])

