import json
import typing as t
from collections import defaultdict


class CaseInsensitiveDict(dict):
    @staticmethod
    def _scrub_key(key: str) -> str:
        return key.lower().replace("-", "_")

    def __setitem__(self, key: t.Any, value: t.Any) -> None:
        if not isinstance(key, str):
            raise TypeError("Key must be a string")
        super().__setitem__(self._scrub_key(key), value)

    def __getitem__(self, key: t.Any) -> t.Any:
        if not isinstance(key, str):
            raise TypeError("Key must be a string")
        return super().__getitem__(self._scrub_key(key))

    def __delitem__(self, key: t.Any) -> None:
        if not isinstance(key, str):
            raise TypeError("Key must be a string")
        return super().__delitem__(self._scrub_key(key))

    def __contains__(self, key: t.Any) -> bool:
        if not isinstance(key, str):
            return False
        return super().__contains__(self._scrub_key(key))


class Context:
    def __init__(self) -> None:
        self._storage: dict[Markdown, dict[str, t.Any]] = defaultdict(
            CaseInsensitiveDict
        )

    def __get__(self, instance: "Markdown", _: t.Type["Markdown"]) -> dict[str, t.Any]:
        return self._storage[instance]

    def __set__(self, instance: "Markdown", ctx: dict[str, t.Any]) -> None:
        for key, value in ctx.items():
            self._storage[instance][key] = value

    def __delete__(self, instance: "Markdown") -> None:
        del self._storage[instance]


class Markdown:
    __ignore__: bool = False
    __regex__: str = r"^([^ ](?:.|\n(?<!\n))*)"

    precedence: float = 0.0

    ctx: dict[str, t.Any] = t.cast(dict[str, t.Any], Context())

    parent: t.Optional["Markdown"] = None
    previous_sibling: t.Optional["Markdown"] = None
    next_sibling: t.Optional["Markdown"] = None

    def __init__(self, ctx: dict[str, t.Any]) -> None:
        self.ctx = ctx

    @property
    def children(self) -> list["Renderable"]:
        return []

    def __contains__(self, other: t.Any) -> bool:
        return other in self.children

    def __hash__(self) -> int:
        return hash(self.dumps())

    @classmethod
    def classes(cls) -> list[t.Type["Markdown"]]:
        for _cls in sorted(
            (_cls for _cls in cls.__subclasses__() if not _cls.__ignore__),
            key=lambda __cls: __cls.precedence,
        ):
            yield from _cls.classes()
            yield _cls

    def dumps(self, *_, **__) -> str:
        raise NotImplementedError

    @classmethod
    def loads(_, content: str) -> "MarkdownType":
        raise NotImplementedError


MarkdownType = t.Union[Markdown, str]
Renderable = t.Union[
    Markdown,
    str,
    list[Markdown | str],
    list[Markdown],
    list[str],
]  # type: ignore[misc]


class Comment(Markdown):
    __regex__: str = r"^<!--(.+?)-->"

    def __init__(self, content: str) -> None:
        self.content = content
        try:
            data = json.loads(content)
        except json.decoder.JSONDecodeError:
            super().__init__({})
        else:
            super().__init__({"data": data})

    def dumps(self, *_, **__) -> str:
        if self.ctx.get("data"):
            return f"<!--{json.dumps(self.ctx['data'])}-->"
        return f"<!--{self.content}-->"

    @classmethod
    def loads(cls, content: str) -> "MarkdownType":
        return Comment(content)


class Text(Markdown):
    precedence: float = 1.0

    def __init__(
        self,
        *elements: Renderable,
    ) -> None:
        self.elements = [
            element if not isinstance(element, str) else element.strip()
            for element in elements
        ]
        super().__init__({})

    def __eq__(self, other: t.Any) -> bool:
        if not isinstance(other, (Text, str)):
            return False
        if isinstance(other, str):
            return other == self.dumps()
        return self.elements == other.elements

    def __hash__(self) -> int:
        return hash(self.dumps())

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}({', '.join(map(repr, self.elements))})"

    @property
    def children(self) -> list["Renderable"]:
        return self.elements

    def dumps(self, *args: t.Any, **kwargs: t.Any) -> str:
        # Prevents circular import!
        from ..serialize import dumps  # pylint: disable=import-outside-toplevel

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
    def loads(  # pylint: disable=arguments-differ
        cls,
        *elements: "MarkdownType",
    ) -> "MarkdownType":
        return cls(*elements)
