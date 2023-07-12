# Test find, findall, and finditer

from lemon import *

TABLE = Table(
    [
        ["Row 1 Column 1", "Row 1 Column 2", "Row 1 Column 3"],
        ["Row 2 Column 1", "Row 2 Column 2", "Row 2 Column 3"],
        ["Row 3 Column 1", "Row 3 Column 2", "Row 3 Column 3"],
    ],
    ["Column 1", "Column 2", "Column 3"],
    alignment=["left", "center", "right"],
    element_id="table-1",
)
LINK = Link("Lemon's Repo", "https://github.com/GrandMoff100/Lemon")

DOCUMENT = indexed_renderable(
    [
        Header("Hello World"),
        Text("This is a paragraph."),
        Bold("This is bold text."),
        Italics("This is italic text."),
        Strikethrough("This is strikethrough text."),
        TABLE,
        LINK,
    ]
)


def test_find():
    assert find(DOCUMENT, Text) == Text("This is a paragraph.")
    assert find(DOCUMENT, Header) == Header("Hello World")
    assert find(DOCUMENT, Bold) == Bold("This is bold text.")
    assert find(DOCUMENT, Italics) == Italics("This is italic text.")
    assert find(DOCUMENT, Strikethrough) == Strikethrough("This is strikethrough text.")
    assert find(DOCUMENT, element_id="table-1") == TABLE
    assert find(DOCUMENT, query="Repo") == LINK


def test_findall():
    assert findall(DOCUMENT, Text) == [Text("This is a paragraph.")]
    assert findall(DOCUMENT, Header) == [Header("Hello World")]
    assert findall(DOCUMENT, Bold) == [Bold("This is bold text.")]
    assert findall(DOCUMENT, Italics) == [Italics("This is italic text.")]
    assert findall(DOCUMENT, Strikethrough) == [
        Strikethrough("This is strikethrough text.")
    ]
    assert findall(DOCUMENT, element_id="table-1") == [TABLE]
    assert findall(DOCUMENT, query="Repo") == [LINK]


def test_finditer():
    for element in finditer(DOCUMENT, Markdown):
        assert isinstance(element, Markdown)


def test_siblings():
    assert LINK.next_sibling is None
    assert LINK.previous_sibling == TABLE
    assert find(DOCUMENT, Text).next_sibling == Bold("This is bold text.")
    assert find(DOCUMENT, Text).previous_sibling == Header("Hello World")
    assert find(DOCUMENT, Header).next_sibling == Text("This is a paragraph.")
    assert find(DOCUMENT, Header).previous_sibling is None
    assert find(DOCUMENT, Bold).next_sibling == Italics("This is italic text.")
    assert find(DOCUMENT, Table).next_sibling.previous_sibling == find(DOCUMENT, Table)
