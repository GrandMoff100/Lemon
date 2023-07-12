import re
import typing as t

from .markdown import Markdown, MarkdownType, Renderable
from .serialize import dumps, loads


def pad(element: Renderable, *args: t.Any, **kwargs: t.Any) -> str:
    return f"  {dumps(element, *args, **kwargs, inline=True)}  "


def match_alignment(alignment: str) -> str:
    if re.search(r":-+:", alignment):
        return "center"
    if re.search(r":-+", alignment):
        return "right"
    if re.search(r"-+:", alignment):
        return "left"
    return "default"


def extract(
    raw_headers: str,
    raw_alignment: str,
    raw_rows: str,
) -> tuple[list[list[MarkdownType]], list[MarkdownType], list[str]]:
    _, *columns, _ = map(str.strip, raw_headers.split("|"))
    _, *alignment, _ = map(str.strip, raw_alignment.split("|"))
    rows = []
    for row in raw_rows.splitlines():
        _, *elements, _ = map(str.strip, row.split("|"))
        rows.append(
            list(
                map(
                    lambda element: t.cast(list[Markdown | str], loads(element))[0],
                    elements,
                )
            )
        )
    return (
        rows,
        list(
            map(lambda column: t.cast(list[Markdown | str], loads(column))[0], columns)
        ),
        list(map(match_alignment, alignment)),
    )


class Table(Markdown):
    __regex__: str = r"(\|(?:.+\|)+)\n\|(:?-+:?\|)+\n((?:\|(?:.+\|)+\n)+)"

    def __init__(
        self,
        rows: t.Sequence[t.Sequence[Renderable]],
        columns: t.Sequence[Renderable],
        alignment: t.Sequence[str] = (),
        element_id: str | None = None,
    ) -> None:
        self.columns = tuple(columns)
        self.rows = tuple(tuple(row) for row in rows)
        self.alignment = alignment if alignment else ("default",) * len(columns)
        self._element_id = element_id
        if element_id is not None:
            super().__init__({"element-id": element_id})
        else:
            super().__init__({})

    def __repr__(self) -> str:
        return f"<{self.__class__.__qualname__} columns={self.columns!r} entries={self.height - 1}>"

    def __eq__(self, other: t.Any) -> bool:
        if not isinstance(other, Table):
            return False
        return (
            self.columns == other.columns
            and self.rows == other.rows
            and self.element_id == other.element_id
        )

    def __hash__(self) -> int:
        return hash(self.dumps())

    @property
    def width(self) -> int:
        return len(self.columns)

    @property
    def height(self) -> int:
        return len(self.rows) + 1

    @property
    def element_id(self) -> str | None:
        return self._element_id

    def dumps(
        self,
        *args: t.Any,
        **kwargs: t.Any,
    ) -> str:
        headers = [pad(header, *args, **kwargs) for header in self.columns]
        alignment = [
            (":" if alignment in ("left", "center") else "")
            + "-" * len(item)
            + (":" if alignment in ("right", "center") else "")
            for item, alignment in zip(headers, self.alignment)
        ]
        table = [
            f"|{'|'.join(headers)}|",
            f"|{'|'.join(alignment)}|",
        ] + [
            f"|{'|'.join([pad(item, *args, **kwargs) for item in row])}|"
            for row in self.rows
        ]
        return "\n" + "\n".join(table) + "\n\n"

    @classmethod
    def loads(  # type: ignore[override]  # pylint: disable=arguments-differ
        cls,
        ctx: t.Optional[dict[str, t.Any]],
        raw_headers: str,
        raw_alignment: str,
        raw_rows: str,
    ) -> MarkdownType:
        element_id = ctx.get("element-id") if ctx is not None else None
        rows, columns, alignment = extract(raw_headers, raw_alignment, raw_rows)
        return cls(rows, columns, alignment, element_id=element_id)
