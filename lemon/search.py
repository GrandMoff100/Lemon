from collections import abc
from typing import Any, Generator, Type, cast

from .markdown.markdown import Markdown, MarkdownType, Renderable


def _match_query(
    markdown: Markdown,
    tag: Type[Markdown] | None,
    query: MarkdownType | None,
    **ctx: Any,
) -> bool:
    conditions = []
    if tag is not None:
        conditions.append(
            type(markdown) == tag  # pylint: disable=unidiomatic-typecheck
        )
    if query is not None:
        conditions.append(query in markdown)
    if ctx:
        conditions.append(
            all(
                markdown.ctx[key] == value if key in markdown.ctx else False
                for key, value in ctx.items()
            )
        )
    return all(conditions)


def finditer(
    markdown: Renderable | list[Renderable],
    tag: Type[Markdown] | None = None,
    query: MarkdownType | None = None,
    parent: Renderable | None = None,
    **ctx: Any,
) -> Generator[Renderable, None, None]:
    if isinstance(markdown, Markdown):
        if _match_query(markdown, tag=tag, query=query, **ctx):
            yield markdown
        if markdown.__children__:
            yield from finditer(
                markdown.__children__, tag=tag, query=query, **ctx, parent=markdown
            )
    elif isinstance(markdown, str):
        if isinstance(query, str):
            if query in markdown:
                if parent is not None:
                    yield parent
                else:
                    yield markdown
    elif isinstance(markdown, abc.Iterable):
        for item in markdown:
            yield from finditer(
                item, tag=tag, query=query, **ctx, parent=cast(Renderable, parent)
            )


def findall(
    markdown: Renderable,
    tag: Type[Markdown] | None = None,
    query: MarkdownType | None = None,
    **ctx: Any,
) -> list[Renderable]:
    return list(finditer(markdown, tag=tag, query=query, **ctx))


def find(
    markdown: Renderable,
    tag: Type[Markdown] | None = None,
    query: MarkdownType | None = None,
    **ctx: Any,
) -> Renderable | None:
    for item in finditer(markdown, tag=tag, query=query, **ctx):
        return item
    return None
