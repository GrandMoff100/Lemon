import json
import typing as t
from collections import abc

from .markdown import Markdown, MarkdownType, Renderable
from .parse import build_lexer, clean, construct


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
    elif isinstance(content, str):
        result += content
        if inline is False:
            result += "\n\n"
    elif isinstance(content, abc.Iterable):
        for item in content:
            result += dumps(item, *args, **kwargs)
    return result


def loads(content: str) -> t.List[MarkdownType]:
    lexer = build_lexer()
    lexer.input(content)  # type: ignore[no-untyped-call]
    lookup = {cls.__qualname__.upper(): cls for cls in Markdown._classes()}
    return clean([construct(token.value, lookup[token.type]) for token in lexer])
