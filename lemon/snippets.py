import typing as t

from .markdown import Markdown


class CodeSnippet(Markdown):
    __regex__: str = r"```((?:.*)?)\n((?:.|\n)+)```"

    def __init__(self, content: str, language: t.Optional[str] = None) -> None:
        self.language = language
        self.content = content.strip()

    def __repr__(self) -> str:
        params = [repr(param) for param in [self.language] if param]
        return f"{self.__class__.__qualname__}({', '.join([repr(self.content)[:30] + '...', *params])})"

    def __eq__(self, other: t.Any) -> bool:
        if not isinstance(other, CodeSnippet):
            return False
        return self.language == other.language and self.content == other.content

    def dumps(self, *_: t.Any, **__: t.Any) -> str:
        return f"```{self.language if self.language else ''}\n{self.content}\n```\n"

    @classmethod
    def loads(cls, ctx: t.Optional[t.Dict[str, t.Any]], language: str, content: str) -> Markdown:  # type: ignore[override]
        language = language.strip()
        return cls(content, None if not language else language)
