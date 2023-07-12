import json
import re
import typing as t
from collections import abc

from .codeblock import CodeBlock
from .markdown import Markdown, Renderable
from .parse import build_lexer, construct, scrub

CLEANING_IGNORE_PATTERNS = [
    r"<!--.*?-->",  # HTML comments
    CodeBlock.__regex__,  # Code blocks
]

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
            if match := re.search(pattern, new_rendered, flags=flags):
                if any(
                    ignore_match.start() <= match.start() <= ignore_match.end()
                    for ignore_pattern in CLEANING_IGNORE_PATTERNS
                    for ignore_match in re.finditer(
                        ignore_pattern, new_rendered, flags=flags
                    )
                ):
                    continue
                new_rendered = re.sub(pattern, replacement, new_rendered, flags=flags)
        if new_rendered != rendered:
            rendered = new_rendered
        else:
            break
    return rendered


def indexed_renderable(renderable: Renderable) -> Renderable:
    _asign_parents(renderable)
    _asign_siblings(renderable)
    return renderable


def _asign_parents(renderable: Renderable) -> None:
    if isinstance(renderable, Markdown):
        for child in renderable.__children__:
            if isinstance(child, Markdown):
                child.parent = renderable
                _asign_parents(child)
    elif isinstance(renderable, abc.Iterable):
        for child in renderable:
            _asign_parents(child)


def _asign_siblings(renderable: Renderable) -> None:
    if isinstance(renderable, Markdown):
        for child in renderable.__children__:
            _asign_siblings(child)
    elif isinstance(renderable, abc.Iterable):
        prev = None
        for child in renderable:
            if prev is not None:
                prev.next_sibling = child
                child.previous_sibling = prev
            prev = child


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
    return indexed_renderable(
        scrub([construct(token.value, lookup[token.type]) for token in lexer])
    )


def dump(content: Renderable, file: t.TextIO, *args: t.Any, **kwargs: t.Any) -> None:
    with file:
        file.write(dumps(content, *args, **kwargs))


def load(file: t.TextIO) -> Renderable:
    with file:
        return loads(file.read())
