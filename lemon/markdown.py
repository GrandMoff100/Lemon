import json
import typing as t
from collections import abc


class Markdown:
    __ignore__: bool = False
    __regex__: str = r"((?:.|\n(?<!\n))+)"
    __ctx_regex__: str = r"(?:<!--(\{.+\})-->\n)?"

    def __init__(self, *elements: "Renderable", ctx: t.Dict[str, t.Any] = {}) -> None:
        self.elements = [
            element if not isinstance(element, str) else element.strip()
            for element in elements
        ]

    def __eq__(self, other: t.Any) -> bool:
        if not isinstance(other, Markdown):
            return False
        if not hasattr(other, "elements"):
            return False
        return self.elements == other.elements

    def __repr__(self) -> str:
        if type(self) == Markdown:
            return f"Markdown({', '.join(map(repr, self.elements))})"
        return f"{self.__class__.__qualname__}()"

    @property
    def data(self) -> t.Dict[str, t.Any]:
        return {}

    def dumps(self, *args: t.Any, **kwargs: t.Any) -> str:
        # Prevents circular import!
        from .serialize import dumps

        kwargs["inline"] = True
        return " ".join(
            [
                dumps(
                    element,
                    *args,
                    **kwargs,
                )
                for element in self.elements
            ]
        )

    @classmethod
    def loads(
        cls,
        ctx: t.Optional[t.Dict[str, t.Any]],
        *elements: "MarkdownType",
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

    def __init__(self) -> None:
        pass

    @staticmethod
    def dumps(*_: t.Any, **__: t.Any) -> str:
        return "\n"

    @classmethod
    def loads(cls, ctx: t.Dict[str, t.Any]) -> MarkdownType:  # type: ignore[override]
        return cls()
