import json
import typing as t

from .markdown import Markdown, MarkdownType, Renderable, dumps


def pad(element: MarkdownType, *args: t.Any, **kwargs: t.Any) -> str:
    return f"  {dumps(element, *args, **kwargs)}  "


class Table(Markdown):
    __regex__: str = r"(?P<columns>\|(?:.+\|)+)\n\|(?:-+\|)+(?P<rows>\n\|(?:.+\|)+)+"

    def __init__(
        self,
        rows: t.Iterable[t.Iterable[MarkdownType]],
        table_id: t.Optional[str] = None,
    ) -> None:
        self.columns, *self.rows = tuple([tuple(row) for row in rows])
        self.table_id = table_id

    @property
    def width(self) -> int:
        return len(self.columns)

    @property
    def height(self) -> int:
        return len(self.rows) + 1

    def data(self) -> t.Dict[str, str]:
        return {
            "type": "table",
            "table-id": self.table_id if self.table_id is not None else "",
        }

    def dumps(
        self,
        *args: t.Any,
        metadata: bool = False,
        **kwargs: t.Any,
    ) -> Renderable:
        if metadata:
            yield f"<!--{json.dumps(self.data)}-->"

        headers = [pad(header, *args, **kwargs) for header in self.columns]

        yield f"|{'|'.join(headers)}|"
        yield f"|{'|'.join(['-' * len(item) for item in headers])}|"
        for row in self.rows:
            yield f"|{'|'.join([pad(item, *args, **kwargs) for item in row])}|"
