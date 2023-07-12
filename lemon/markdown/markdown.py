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
    __regex__: str = r"((?:.|\n(?<!\n))+)"
    __ctx_regex__: str = r"(?:<!--(\{.+\})-->\n)?"

    ctx: dict[str, t.Any] = t.cast(dict[str, t.Any], Context())

    parent: t.Optional["Markdown"] = None
    previous_sibling: t.Optional["Markdown"] = None
    next_sibling: t.Optional["Markdown"] = None

    def __init__(self, ctx: dict[str, t.Any]) -> None:
        self.ctx = ctx

    @property
    def __children__(self) -> list["Renderable"]:
        return []

    def __contains__(self, other: t.Any) -> bool:
        return other in self.__children__

    def __hash__(self) -> int:
        return hash(self.dumps())

    @classmethod
    def classes(cls) -> list[t.Type["Markdown"]]:
        _classes = cls.__subclasses__()
        return [_cls for _cls in _classes if not _cls.__ignore__]

    def dumps(self, *_, **__) -> str:
        return ""

    @classmethod
    def loads(cls, ctx: dict[str, t.Any] | None, content: str) -> "MarkdownType":
        return Text.loads(ctx, content)


MarkdownType = t.Union[Markdown, str]
Renderable = t.Union[
    Markdown,
    str,
    list[Markdown | str],
    list[Markdown],
    list[str],
]  # type: ignore[misc]


class Newline(Markdown):
    __regex__: str = r"\n"

    def __init__(self) -> None:
        super().__init__({})

    @staticmethod
    def dumps(*_: t.Any, **__: t.Any) -> str:
        return "\n"

    @classmethod
    def loads(cls, _: dict[str, t.Any]) -> MarkdownType:  # type: ignore[override]  # pylint: disable=arguments-differ
        return cls()


class Text(Markdown):
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
    def __children__(self) -> list["Renderable"]:
        return self.elements

    def dumps(self, *args: t.Any, **kwargs: t.Any) -> str:
        # Prevents circular import!
        from .serialize import dumps  # pylint: disable=import-outside-toplevel

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
    def loads(  # pylint: disable=arguments-differ
        cls,
        _: dict[str, t.Any] | None,
        *elements: "MarkdownType",
    ) -> "MarkdownType":
        return cls(*elements)
