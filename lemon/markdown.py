import typing as t
from collections import abc


class Markdown:
    def __init__(self, *elements: Renderable) -> None:
        self.elements = elements

    def render(self, *args, **kwargs) -> "Renderable":
        yield " ".join([render(element, *args, **kwargs) for element in self.elements])


MarkdownType = t.Union[Markdown, str]
Renderable = t.Union[MarkdownType, t.Iterable[MarkdownType]]


def render(content: Renderable, *args, **kwargs) -> str:
    if isinstance(content, Markdown):
        return render(content.render(*args, **kwargs), *args, **kwargs)
    if isinstance(content, str):
        return content
    if isinstance(content, abc.Iterable):
        return "\n\n".join([render(item, *args, **kwargs) for item in content])
