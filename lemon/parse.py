import json
import re
import typing as t
from functools import reduce
import operator as op

from .lex import lex
from .markdown import Markdown, MarkdownType, Newline, Renderable
from .style import StyleMixin


def tokens() -> t.Dict[str, t.Type[Markdown]]:
    return {cls.__qualname__.upper(): cls for cls in Markdown._classes()}


def token_regex() -> t.Generator[t.Tuple[str, str], None, None]:
    for name, cls in tokens().items():
        yield f"t_{name}", cls.__ctx_regex__ + cls.__regex__


def lex_error(token) -> None:
    raise ValueError(token)


def build_lexer():
    order_preserved_attributes = (
        ("tokens", tuple(tokens())),
        ("t_error", lex_error),
        *token_regex(),
    )
    cls = type("Lexer", (), {})
    for name, value in order_preserved_attributes:
        setattr(cls, name, value)
    return lex(module=cls)


def extract(value, cls):
    match = re.fullmatch(
        cls.__ctx_regex__ + cls.__regex__,
        value,
    )
    assert match is not None
    ctx, *params = match.groups()
    return ctx, params


def subdivide(markdown: Markdown) -> Markdown:
    source, *_ = markdown.elements
    assert isinstance(source, str)
    elements: t.List[MarkdownType] = []

    try:
        (match, style_class), *_ = sorted(
            filter(
                lambda pair: pair[0] is not None,
                [
                    (
                        t.cast(re.Match, re.search(style_class.__regex__, source)),
                        style_class,
                    )
                    for style_class in StyleMixin.__subclasses__()
                ],
            ),
            key=lambda pair: pair[0].start(),
        )
        sub_content = match.string[match.start() : match.end()]
        pre, source = source.split(sub_content)
        if pre.strip():
            elements += [pre]
        elements += [
            construct(sub_content, style_class),
            *subdivide(Markdown(source)).elements, # type: ignore[list-item]
        ]
    except ValueError:
        if source.strip():
            elements.append(source.strip())
    finally:
        return Markdown(*elements)


def construct(value, cls) -> MarkdownType:
    ctx, params = extract(value, cls)
    if ctx is not None:
        ctx = json.loads(ctx)
    element = cls.loads(ctx, *params)
    if type(element) == Markdown:
        return subdivide(element)
    return element


def clean(tree: t.List[MarkdownType]) -> t.List[MarkdownType]:
    tree = [
        element
        for element in tree
        if not (isinstance(element, str) and element == " " * len(element))
    ]
    tree = [element for element in tree if not isinstance(element, Newline)]
    return tree


def loads(content: str) -> t.List[MarkdownType]:
    lexer = build_lexer()
    lexer.input(content)
    lookup = {cls.__qualname__.upper(): cls for cls in Markdown._classes()}
    return clean([construct(token.value, lookup[token.type]) for token in lexer])
