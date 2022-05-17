import typing as t
from .markdown import Markdown, MarkdownType


class Table(Markdown):
    def __init__(self, rows: t.Iterable[t.Iterable[MarkdownType]]):
        for row in rows:
            for item in row:
                pass
