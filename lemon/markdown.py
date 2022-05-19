import json
import typing as t
from collections import abc


class Markdown:
    __ignore__: bool = False
    __regex__: str = r"((?:.|\n(?<!\n))+)"
    __ctx_regex__: str = r"(?:<!--(\{.+\})-->\n)?"

    def __init__(self, *elements: "Renderable", ctx: t.Dict[str, t.Any] = {}) -> None:
        self.elements = [element if not isinstance(element, str) else element.strip() for element in elements]

    def __repr__(self) -> str:
        if type(self) == Markdown:
            return f"Markdown({', '.join(map(repr, self.elements))})"
        return f"{self.__class__.__qualname__}()"

    @property
    def data(self) -> t.Dict[str, t.Any]:
        return {}

    def dumps(self, *args: t.Any, **kwargs: t.Any) -> str:
        kwargs["inline"] = True
        return (
            "".join(
                [
                    dumps(
                        element,
                        *args,
                        **kwargs,
                    )
                    for element in self.elements
                ]
            )
            + "\n\n"
        )

    @classmethod
    def loads(
        cls, ctx: t.Dict[str, t.Any], *elements: "MarkdownType"
    ) -> "MarkdownType":
        return Markdown(*elements)

    @classmethod
    def _classes(cls) -> t.List[t.Type["Markdown"]]:
        _classes = cls.__subclasses__() + [cls]
        return [_cls for _cls in _classes if not _cls.__ignore__]


MarkdownType = t.Union[Markdown, str]
Renderable = t.Union[MarkdownType, t.Iterable[MarkdownType]]


class Newline(Markdown):
    __regex__: str = r"\n"

    def __init__(self):
        pass

    def dumps(self, *_, **__) -> str:
        return "\n"

    @classmethod
    def loads(cls, ctx: t.Dict[str, t.Any]) -> MarkdownType:  # type: ignore[override]
        return cls()


def dumps(
    content: Renderable,
    *args: t.Any,
    inline: bool = False,
    **kwargs: t.Any,
) -> str:
    result = ""
    if isinstance(content, Markdown):
        if content.data:
            result += f"<!--{json.dumps(content.data)}-->\n"
        result += content.dumps(*args, **kwargs)
        result += " "
    elif isinstance(content, str):
        result += content
        if inline is False:
            result += "\n\n"
        else:
            result += " "
    elif isinstance(content, abc.Iterable):
        kwargs["inline"] = True
        for item in content:
            result += dumps(item, *args, **kwargs)
    return result
