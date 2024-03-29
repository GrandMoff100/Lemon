# pylint: disable=R0801
from lemon import (
    Bold,
    CodeBlock,
    Header,
    InlineCode,
    Italics,
    Link,
    Strikethrough,
    Table,
    Text,
    dumps,
)


def test_header() -> None:
    document = Header(
        "My Awesome Project",
        [
            "This project is so awesome that you should go star it on GitHub!",
            Header("Description", "You can implement nested sub-headers like magic!"),
        ],
    )
    expected = (
        "# My Awesome Project\n\n"
        "This project is so awesome that you should go star it on GitHub!\n\n"
        "## Description\n\n"
        "You can implement nested sub-headers like magic!\n\n"
    )
    assert dumps(document) == expected


def test_bold_italics_strikethrough() -> None:
    document = Text(
        Bold("My bold text"),
        Italics("is italisized"),
        "this is not",
        Strikethrough("and also strikethrough"),
        "and more regular text",
        InlineCode("python -m code"),
        Bold("But bold again"),
        Strikethrough("and then strikethrough"),
        Italics("and finally more italics."),
        "finally some regular text.",
    )

    assert dumps(document) == (
        "**My bold text** "
        "*is italisized* "
        "this is not "
        "~~and also strikethrough~~ "
        "and more regular text "
        "``python -m code`` "
        "**But bold again** "
        "~~and then strikethrough~~ "
        "*and finally more italics.* "
        "finally some regular text."
    )


def test_table() -> None:
    data = Table(
        [
            ["Ted", "New York", "Busy"],
            ["Angie", "France", "Free"],
        ],
        ["Name", "Location", "Status"],
    )

    assert dumps(data) == (
        "\n"
        "| Name | Location | Status |\n"
        "|--------|------------|----------|\n"
        "| Ted | New York | Busy |\n"
        "| Angie | France | Free |\n"
        "\n"
    )


def test_inline_code():
    document = Text(
        "The most telling sign of a python beginner is the use of",
        InlineCode("range(len(obj))"),
        "vs",
        InlineCode("enumerate(obj)"),
        ".",
    )
    assert dumps(document) == (
        "The most telling sign of a "
        "python beginner is the use of "
        "``range(len(obj))`` vs ``enumerate(obj)`` ."
    )


def test_code_snippet():
    document = CodeBlock(
        """
import math

def topsecretcode():
    print("Hello World")

foobar()
""",
        "python",
    )
    expected = (
        "```python\n"
        "import math\n"
        "\n"
        "def topsecretcode():\n"
        '    print("Hello World")\n'
        "\n"
        "foobar()\n"
        "```\n"
    )

    assert dumps(document) == expected


def test_links():
    link = Link(
        Link(
            "",
            "https://example.com/foobars-are-tasty.png",
            media=True,
        ),
        "https://somewebsite.com/",
    )

    assert (
        dumps(link)
        == "[![](https://example.com/foobars-are-tasty.png)](https://somewebsite.com/)"
    )
