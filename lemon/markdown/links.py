import typing as t

from .markdown import Markdown, MarkdownType
from .serialize import dumps, loads


class Link(Markdown):
    __regex__: str = r'(!?)\[(.*(?!.*\[(?!.*\])))\]\((.+?) ?((?:".+?")?)\)'

    def __init__(
        self,
        face: MarkdownType,
        path: str,
        title: str | None = None,
        media: bool = False,
    ) -> None:
        self.face = face
        self.path = path
        self.title = title
        self.media = media
        super().__init__({})

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__qualname__}"
            f"({self.face!r}, {self.path!r}, media={self.media!r}, title={self.title!r})"
        )

    def __eq__(self, other: t.Any) -> bool:
        if not isinstance(other, Link):
            return False
        return (
            self.face == other.face
            and self.path == other.path
            and self.title == other.title
            and self.media == other.media
        )

    def dumps(self, *args, **kwargs) -> str:
        media = "!" if self.media else ""
        face = dumps(self.face, *args, **kwargs).strip()
        if self.title is not None:
            path = f"{self.path} {self.title}"
        else:
            path = self.path
        return f"{media}[{face}]({path})"

    @classmethod
    def loads(  # type: ignore[override]  # pylint: disable=arguments-differ, too-many-arguments
        cls,
        ctx: dict[str, t.Any] | None,
        media: str,
        face: str,
        path: str,
        title: str | None,
    ) -> MarkdownType:
        if not title:
            title = None
        return cls(
            face=t.cast(list[Markdown | str], loads(face))[0],
            path=path,
            title=title,
            media=bool(media),
        )
