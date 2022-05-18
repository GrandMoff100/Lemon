import json
import re
import typing as t

from .lex import lex
from .markdown import Markdown, MarkdownType, Newline, Renderable


def token_lookup() -> t.Dict[str, t.Type[Markdown]]:
    return {
        cls.__qualname__.upper(): cls for cls in Markdown.__subclasses__() + [Markdown]
    }


def all_tokens() -> t.Tuple[str, ...]:
    return tuple(
        sorted(
            token_lookup(),
            key=lambda name: 0
            if name not in Markdown.__precedence__
            else Markdown.__precedence__.index(name),
        )
    )


def token_regex() -> t.Generator[t.Tuple[str, str], None, None]:
    lookup = token_lookup()
    for name in all_tokens():
        cls = lookup[name]
        yield f"t_{name}", cls.__ctx_regex__ + cls.__regex__


def lex_error(token) -> None:
    raise ValueError(token)


def build_lexer():
    order_preserved_attributes = (
        ("tokens", all_tokens()),
        ("t_error", lex_error),
        *token_regex(),
    )
    cls = type("Lexer", (), dict(order_preserved_attributes))
    return lex(module=cls)


def construct(token) -> MarkdownType:
    cls = token_lookup()[token.type]
    match = re.fullmatch(cls.__ctx_regex__ + cls.__regex__, token.value)
    assert match is not None
    ctx, *params = match.groups()
    if ctx is not None:
        ctx = json.loads(ctx)
    return cls.loads(ctx, *params)


def clean(tree: t.List[MarkdownType]) -> t.List[MarkdownType]:
    return [element for element in tree if not isinstance(element, Newline)]


def loads(content: str) -> t.List[MarkdownType]:
    lexer = build_lexer()
    lexer.input(content)
    return clean([construct(token) for token in lexer])
