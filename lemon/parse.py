from .sly.lex import Lexer  # type: ignore[attr-defined]
from .markdown import Renderable


class LemonLexer(Lexer):
    pass


def loads(content: str) -> Renderable:
    pass