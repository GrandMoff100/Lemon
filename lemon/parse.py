import json
import re
import typing as t


from .markdown.markdown import Markdown, MarkdownType, Text
from .markdown.style import StyleMixin


class Lexer:
    ignore: str = " \t\n"

    def __init__(self):
        self.tokens = {cls.__qualname__.upper(): cls for cls in Markdown.classes()}

    def reverse_accumulate(self, content: str) -> t.Generator[str, None, None]:
        """Reverse accumulate a string."""
        for index in range(len(content), 1, -1):
            yield content[:index]

    def parse(self, content: str) -> t.Generator[tuple[str, re.Match], None, None]:
        """Parse a string into tokens."""
        while content:
            if content[0] in self.ignore:
                content = content[1:]
                continue
            elif match := self.find(content):
                yield match
                _, match_obj = match
                content = content[match_obj.end(0) :]
            else:
                raise ValueError(
                    f"No token or ignore character in {content!r}. Parsing failed."
                )

    def find(self, content: str) -> tuple[str, re.Match] | None:
        """Find all token matches in a string."""
        print("start find")
        current_match = None
        for candidate in self.reverse_accumulate(content):
            matches: list[tuple[str, re.Match]] = []
            for token, cls in self.tokens.items():
                if current_match is not None:
                    # If the current match has a higher precedence, skip this token
                    if self.tokens[current_match[0]].precedence < cls.precedence:
                        continue
                    # If the current match has the same precedence, but is longer, skip this token
                    if self.tokens[
                        current_match[0]
                    ].precedence == cls.precedence and len(candidate) < current_match[1].end(0):
                        continue
                matches += [
                    (token, match) for match in re.finditer(cls.__regex__, candidate)
                ]
            if not matches:
                continue

            min_precedence = min(self.tokens[token].precedence for token, _ in matches)
            potential_match = sorted(
                (
                    (token, match)
                    for token, match in matches
                    if self.tokens[token].precedence == min_precedence
                ),
                key=lambda pair: pair[1].string,
            )[0]

            if current_match is None:
                current_match = potential_match
            elif self.tokens[potential_match[0]].precedence >= self.tokens[
                current_match[0]
            ].precedence and potential_match[1].end(0) > current_match[1].end(0):
                current_match = potential_match
        print("end find")
        return current_match


def subdivide_inline_text(markdown: Text) -> Text:
    """Subdivide an inline Text with one string element into a Text object with multiple elements."""
    source, *_ = markdown.elements
    assert isinstance(source, str)
    elements: list[MarkdownType] = []
    try:
        (match, style_class), *_ = sorted(
            filter(
                lambda pair: pair[0] is not None,
                [
                    (
                        t.cast(t.Match[str], re.search(style_class.__regex__, source)),
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
            *subdivide_inline_text(Text(source)).elements,  # type: ignore[list-item]
        ]
    except ValueError:
        if source.strip():
            elements.append(source.strip())
    return Text(*elements)


def construct(match: re.Match, cls: t.Type[Markdown]) -> MarkdownType:
    """Construct a Markdown object from a string."""
    element = cls.loads(*match.groups())
    # Check only for Text objects
    if type(element) == Text:  # pylint: disable=unidiomatic-typecheck
        return subdivide_inline_text(element)
    return element


def scrub(tree: list[MarkdownType]) -> list[MarkdownType]:
    """Remove empty strings from a tree."""
    return [
        element
        for element in tree
        if not (isinstance(element, str) and element == " " * len(element))
    ]
