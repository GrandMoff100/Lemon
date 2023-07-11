import json
import typing as t
from collections import abc

from .markdown import Markdown, Renderable
from .parse import build_lexer, clean, construct


def dumps(
    content: Renderable,
    *args: t.Any,
    inline: bool = False,
    **kwargs: t.Any,
) -> str:
    result = ""
    if isinstance(content, Markdown):  # pylint: disable=unidiomatic-typecheck
        if content.ctx:
            result += f"<!--{json.dumps(content.ctx)}-->\n"
        result += content.dumps(*args, **kwargs)
    elif isinstance(content, str):
        result += content
        if inline is False:
            result += "\n\n"
    elif isinstance(content, abc.Iterable):
        for item in content:
            result += dumps(item, *args, **kwargs)
    return result


def loads(content: str) -> Renderable:
    if content == "":
        return [content]
    lexer = build_lexer()
    lexer.input(content)  # type: ignore[no-untyped-call]
    lookup = {cls.__qualname__.upper(): cls for cls in Markdown.classes()}
    return clean([construct(token.value, lookup[token.type]) for token in lexer])


def dump(content: Renderable, file: t.TextIO, *args: t.Any, **kwargs: t.Any) -> None:
    with file:
        file.write(dumps(content, *args, **kwargs))


def load(file: t.TextIO) -> Renderable:
    with file:
        return loads(file.read())
