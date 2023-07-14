import json
import re
import typing as t
from collections import abc

from .markdown.codeblock import CodeBlock
from .markdown.markdown import Markdown, Renderable
from .parse import Lexer, construct, scrub


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
        for child in renderable.children:
            if isinstance(child, Markdown):
                child.parent = renderable
                _asign_parents(child)
    elif isinstance(renderable, abc.Iterable):
        for child in renderable:
            _asign_parents(child)


def _asign_siblings(renderable: Renderable) -> None:
    if isinstance(renderable, Markdown):
        for child in renderable.children:
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
    clean: bool = True,
    **kwargs: t.Any,
) -> str:
    result = []
    if isinstance(content, Markdown):  # pylint: disable=unidiomatic-typecheck
        result.append(content.dumps(*args, **kwargs, clean=False))
    elif isinstance(content, str):
        result.append(content)
    elif isinstance(content, abc.Iterable):
        for item in content:
            result.append(dumps(item, *args, **kwargs, clean=False))
    if clean:
        return _clean("\n\n".join(result))
    return "\n\n".join(result)


def loads(content: str) -> Renderable:
    if content == "":
        return []
    lexer = Lexer()
    return indexed_renderable(
        scrub(
            [
                construct(string, lexer.tokens[token])
                for token, string in lexer.parse(content)
            ]
        )
    )


def dump(content: Renderable, file: t.TextIO, *args: t.Any, **kwargs: t.Any) -> None:
    with file:
        file.write(dumps(content, *args, **kwargs))


def load(file: t.TextIO) -> Renderable:
    with file:
        return loads(file.read())
