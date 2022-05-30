import typing as t

from .markdown import Markdown, MarkdownType
from .serialize import dumps


def pad(element: MarkdownType, *args: t.Any, **kwargs: t.Any) -> str:
    return f"  {dumps(element, *args, **kwargs, inline=True)}  "


def extract(raw_headers: str, raw_rows: str) -> t.List[t.List[str]]:
    _, *columns, _ = map(str.strip, raw_headers.split("|"))
    rows = [columns]
    for row in raw_rows.splitlines():
        _, *elements, _ = map(str.strip, row.split("|"))
        rows.append(elements)
    return rows


class Table(Markdown):
    __regex__: str = r"(\|(?:.+\|)+)\n\|(?:-+\|)+\n((?:\|(?:.+\|)+\n)+)"

    def __init__(
        self,
        rows: t.Iterable[t.Iterable[MarkdownType]],
        table_id: t.Optional[str] = None,
    ) -> None:
        self.columns, *self.rows = tuple(tuple(row) for row in rows)
        self.table_id = table_id

    def __repr__(self) -> str:
        return f"<{self.__class__.__qualname__} columns={self.columns!r} entries={self.height - 1}>"

    def __eq__(self, other: t.Any) -> bool:
        if not isinstance(other, Table):
            return False
        return (
            self.columns == other.columns
            and self.rows == other.rows
            and self.table_id == other.table_id
        )

    @property
    def width(self) -> int:
        return len(self.columns)

    @property
    def height(self) -> int:
        return len(self.rows) + 1

    @property
    def data(self) -> t.Dict[str, str]:
        if self.table_id:
            return {"table-id": self.table_id}
        return {}

    def dumps(
        self,
        *args: t.Any,
        **kwargs: t.Any,
    ) -> str:
        headers = [pad(header, *args, **kwargs) for header in self.columns]
        table = [
            f"|{'|'.join(headers)}|",
            f"|{'|'.join(['-' * len(item) for item in headers])}|",
        ] + [
            f"|{'|'.join([pad(item, *args, **kwargs) for item in row])}|"
            for row in self.rows
        ]
        return "\n".join(table) + "\n"

    @classmethod
    def loads(  # type: ignore[override]  # pylint: disable=arguments-differ
        cls,
        ctx: t.Optional[t.Dict[str, t.Any]],
        headers: str,
        rows: str,
    ) -> MarkdownType:
        table_id = ctx.get("table-id") if ctx is not None else None
        return cls(extract(headers, rows), table_id=table_id)
