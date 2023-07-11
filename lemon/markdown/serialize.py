import json
import re
import typing as t
from collections import abc

from .markdown import Markdown, Renderable
from .parse import build_lexer, clean, construct

CLEANER_PATTERNS = [
    (r"^ +(.*)$", r"\1", re.MULTILINE),
    (r"^(.*) +$", r"\1", re.MULTILINE),
    (r"\n{3}", r"\n\n", re.NOFLAG),
    (r" {2}", r" ", re.NOFLAG),
]


def _clean(rendered: str) -> str:
    while True:
        new_rendered = rendered
        for pattern, replacement, flags in CLEANER_PATTERNS:
            new_rendered = re.sub(pattern, replacement, new_rendered, flags=flags)
        if new_rendered != rendered:
            rendered = new_rendered
        else:
            break
    return rendered


def dumps(
    content: Renderable,
    *args: t.Any,
    inline: bool = False,
    clean: bool = True,
    **kwargs: t.Any,
) -> str:
    result = ""
    if isinstance(content, Markdown):  # pylint: disable=unidiomatic-typecheck
        if content.ctx:
            result += f"\n\n<!--{json.dumps(content.ctx)}-->"
        result += content.dumps(*args, **kwargs, clean=False)
    elif isinstance(content, str):
        result += content
        if inline is False:
            result += "\n\n"
    elif isinstance(content, abc.Iterable):
        for item in content:
            result += dumps(item, *args, **kwargs, clean=False)
    if clean:
        return _clean(result)
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
