from collections import abc
from typing import Any, Generator, Type

from .markdown.markdown import Markdown, MarkdownType, Renderable


def finditer(
    markdown: Renderable,
    tag: Type[Markdown] | None = None,
    query: MarkdownType | None = None,
    **ctx: Any,
) -> Generator[MarkdownType, None, None]:
    if isinstance(markdown, Markdown):
        conditions = []
        if tag is not None:
            conditions.append(isinstance(markdown, tag))
        if query is not None:
            conditions.append(query in markdown)
        if ctx:
            conditions.append(
                all(markdown.ctx[key] == value for key, value in ctx.items())
            )
        if all(conditions):
            yield markdown
    elif isinstance(markdown, abc.Iterable):
        for item in markdown:
            if (results := finditer(item, tag=tag, query=query, **ctx)) is not None:
                yield from results
    elif isinstance(markdown, str):
        if isinstance(query, str):
            if query in markdown:
                yield markdown


def findall(
    markdown: Renderable,
    tag: Type[Markdown] | None = None,
    query: MarkdownType | None = None,
    **ctx: Any,
) -> list[MarkdownType]:
    return list(finditer(markdown, tag=tag, query=query, **ctx))


def find(
    markdown: Renderable,
    tag: Type[Markdown] | None = None,
    query: MarkdownType | None = None,
    **ctx: Any,
) -> MarkdownType | None:
    for item in finditer(markdown, tag=tag, query=query, **ctx):
        return item
    return None
