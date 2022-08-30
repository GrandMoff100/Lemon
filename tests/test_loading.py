# pylint: disable=R0801
import typing as t

from lemon import (
    Bold,
    CodeSnippet,
    Header,
    InlineCode,
    Italics,
    Link,
    Strikethrough,
    Table,
    Text,
    loads,
)


def test_header() -> None:
    content = (
        "# My Awesome Project\n\n"
        "This project is so awesome that you should go star it on GitHub!\n\n"
        "## Description\n\n"
        "You can implement nested sub-headers like magic!\n\n"
    )
    assert loads(content) == [
        Header(
            "My Awesome Project",
            [
                Text(
                    "This project is so awesome that you should go star it on GitHub!"
                ),
                Header(
                    "Description",
                    [Text("You can implement nested sub-headers like magic!")],
                ),
            ],
        )
    ]


def test_bold_italics_strikethrough() -> None:
    content = (
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

    assert loads(content) == [
        Text(
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
    ]


def test_table() -> None:
    content = (
        "|Name  |  Location|Status|\n"
        "|--------|------------|----------|\n"
        "|  Ted  |  New York  |  Busy  |\n"
        "|  Angie  |  France  |  Free  |\n"
    )

    assert loads(content) == [
        Table(
            [
                ["Ted", "New York", "Busy"],
                ["Angie", "France", "Free"],
            ],
            ["Name", "Location", "Status"],
        )
    ]


def test_table_with_ctx() -> None:
    content = (
        '<!--{"this-attribute": "should-not-exist", "element-id": "testing-table"}-->\n'
        "| a | b |\n"
        "|---------|-------|\n"
        "| Alligator | Bumblebee |\n"
        "| Apple | Blueberry |\n"
    )

    table, *_ = t.cast(list[Table], loads(content))
    assert table.element_id == "testing-table"
    assert "this-attribute" not in table.ctx


def test_inline_code():
    content = (
        "The most telling sign of a python beginner "
        "is the use of ``range(len(obj))`` vs ``enumerate(obj)`` ."
    )

    assert loads(content) == [
        Text(
            "The most telling sign of a python beginner is the use of",
            InlineCode("range(len(obj))"),
            "vs",
            InlineCode("enumerate(obj)"),
            ".",
        )
    ]


def test_code_snippet():
    content = (
        "```python\n"
        "import math\n"
        "\n"
        "def topsecretcode():\n"
        '    print("Hello World")\n'
        "\n"
        "foobar()\n"
        "```\n"
    )

    assert loads(content) == [
        CodeSnippet(
            'import math\n\ndef topsecretcode():\n    print("Hello World")\n\nfoobar()',
            "python",
        )
    ]


def test_links():
    content = (
        "[![](https://example.com/foobars-are-tasty.png)](https://somewebsite.com/)"
    )

    assert loads(content) == [
        Link(
            Link(
                "", "https://example.com/foobars-are-tasty.png", media=True, title=None
            ),
            "https://somewebsite.com/",
            media=False,
            title=None,
        )
    ]
