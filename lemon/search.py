from typing import Callable
from .markdown import Markdown, MarkdownType, Renderable


def contains(markdown: Renderable, obj: MarkdownType) -> bool:
    if isinstance(markdown, (Markdown, list)):
        if obj in markdown:
            return True
    if isinstance(markdown, list):
        for item in markdown:
            if contains(item, obj):
                return True
    if isinstance(markdown, str):
        if isinstance(obj, str):
            if obj in markdown:
                return True
    return False


def find(markdown: Renderable, condition: Callable[[MarkdownType], bool]) -> list[Renderable]:
    results = []
    if isinstance(markdown, list):
        for item in markdown:
            result += find(item, condition)
    if isinstance(markdown, Markdown):
        results += find(markdown.__children__, condition)
        if condition(markdown):
            results.append(markdown)
    if isinstance(markdown, str):
        if condition(markdown):
            results.append(markdown)
    return results
