import typing as t

from .markdown import Markdown


class CodeBlock(Markdown):
    __regex__: str = r"```((?:.*)?)\n((?:.|\n)*?)```"

    def __init__(
        self,
        content: str,
        language: str | None = None,
        element_id: str | None = None,
    ) -> None:
        self.language = language
        self.content = content.strip()
        if element_id is not None:
            super().__init__({"element-id": element_id})
        else:
            super().__init__({})

    def __eq__(self, other: t.Any) -> bool:
        if not isinstance(other, CodeBlock):
            return False
        return self.language == other.language and self.content == other.content

    def __repr__(self) -> str:
        params = [repr(param) for param in [self.language] if param]
        repr_params = ", ".join([repr(self.content)[:30] + "...", *params])
        return f"{self.__class__.__qualname__}({repr_params})"

    def dumps(self, *_: t.Any, **__: t.Any) -> str:
        return f"```{self.language if self.language else ''}\n{self.content}\n```\n"

    @classmethod
    def loads(  # type: ignore[override] # pylint: disable=arguments-differ
        cls,
        _: dict[str, t.Any] | None,
        language: str,
        content: str,
    ) -> Markdown:
        language = language.strip()
        return cls(content, language if language else None)
