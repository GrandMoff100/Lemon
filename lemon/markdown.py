import typing as t


class Markdown:
    __ignore__: bool = False
    __regex__: str = r"((?:.|\n(?<!\n))+)"
    __ctx_regex__: str = r"(?:<!--(\{.+\})-->\n)?"

    ctx: t.Dict[str, t.Any]

    def __init__(self, ctx: t.Dict[str, t.Any]) -> None:
        self.ctx = ctx

    @classmethod
    def classes(cls) -> t.List[t.Type["Markdown"]]:
        _classes = cls.__subclasses__()
        return [_cls for _cls in _classes if not _cls.__ignore__]

    def dumps(self, *_, **__) -> str:
        return ""

    @classmethod
    def loads(cls, ctx: t.Optional[t.Dict[str, t.Any]], content: str) -> "MarkdownType":
        return Text.loads(ctx, content)


MarkdownType = t.Union[Markdown, str]
Renderable = t.Union[MarkdownType, t.Iterable[MarkdownType]]


class Newline(Markdown):
    __regex__: str = r"\n"

    def __init__(self) -> None:
        super().__init__({})

    @staticmethod
    def dumps(*_: t.Any, **__: t.Any) -> str:
        return "\n"

    @classmethod
    def loads(cls, _: t.Dict[str, t.Any]) -> MarkdownType:  # type: ignore[override]  # pylint: disable=arguments-differ
        return cls()


class Text(Markdown):
    def __init__(
        self,
        *elements: "Renderable",
    ) -> None:
        super().__init__({})
        self.elements = [
            element if not isinstance(element, str) else element.strip()
            for element in elements
        ]

    def __eq__(self, other: t.Any) -> bool:
        if not isinstance(other, Text):
            return False
        return self.elements == other.elements

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}({', '.join(map(repr, self.elements))})"

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
        _: t.Optional[t.Dict[str, t.Any]],
        *elements: "MarkdownType",
    ) -> "MarkdownType":
        return cls(*elements)
