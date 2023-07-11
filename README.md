# 🍋 Lemon MD 🍋

Easily access, serialize, and synthesize markdown information!

<!--{"element-id": "feature-table"}-->
| Feature | Dumpable | Loadable  |
|---------|----------|-----------|
| Bold | As of Initial Codebase | As of [#4](https://github.com/GrandMoff100/Lemon/pulls/4) |
| Italics | As of Initial Codebase | As of [#4](https://github.com/GrandMoff100/Lemon/pulls/4) |
| Strikethrough | As of [#4](https://github.com/GrandMoff100/Lemon/pulls/4) | As of [#4](https://github.com/GrandMoff100/Lemon/pulls/4) |
| Tables | As of Initial Codebase | As of [#3](https://github.com/GrandMoff100/Lemon/pulls/3) |
| Headers | As of Intitial Codebase | As of [#2](https://github.com/GrandMoff100/Lemon/pulls/2) |
| Inline Code Blocks | As of [#6](https://github.com/GrandMoff100/Lemon/pulls/6) | As of [#6](https://github.com/GrandMoff100/Lemon/pulls/6) |
| Fenced Code Blocks | As of [#6](https://github.com/GrandMoff100/Lemon/pulls/6) | As of [#6](https://github.com/GrandMoff100/Lemon/pulls/6) |
| Blockquotes | Not Yet | Not Yet |
| Links/Images |  As of [#10](https://github.com/GrandMoff100/Lemon/pulls/10) | As of [#10](https://github.com/GrandMoff100/Lemon/pulls/10) |
| Bulleted Lists | Not Yet | Not Yet |
| Ordered Lists | Not Yet | Not Yet |
| Bulleted Checklists | Not Yet | Not Yet |
| Non-Bulleted Checklists | Not Yet | Not Yet |
| Nested Lists/Checklists | Not Yet | Not Yet |
| Horizontal Rule | Not Yet | Not Yet |
| Custom Heading IDs | Not Yet | Not Yet |
| Footnotes | Not Yet | Not Yet |
| Definition List | Not Yet | Not Yet |
| Highlighting | Not Yet | Not Yet |

> Do you like blockquotes? I like blockquotes (and lists). Here's a list in a blockquote:
>
> - This is a list item
> - This is another list item
> - This is a third list item
>

## Installation

```bash
pip install lemon-md
```

## Usage

```python
from lemon import (
    Text,
    Table,
    Bold,
    Italics,
    Strikethrough,
    Link,
    List,
    Checklist,
    HorizontalRule,
    Footnotes,
    DefinitionList,
    Highlighting,
    CodeBlock,
    Blockquote,
    Header,
    InlineCode,
    dumps,
)

document = [
    Header("Hello World"),
    Text("This is a paragraph."),
    Bold("This is bold text."),
    Italics("This is italic text."),
    Strikethrough("This is strikethrough text."),
    Table(
        [
            ["Row 1 Column 1", "Row 1 Column 2", "Row 1 Column 3"],
            ["Row 2 Column 1", "Row 2 Column 2", "Row 2 Column 3"],
            ["Row 3 Column 1", "Row 3 Column 2", "Row 3 Column 3"],
        ],
        ["Column 1", "Column 2", "Column 3"],
        alignment=["left", "center", "right"],
    ),
    Link("Lemon's Repo", "https://github.com/GrandMoff100/Lemon"),
    List(
        [
            "This is a list item.",
            "This is another list item.",
            "This is a third list item.",
        ]
    ),
    Checklist(
        [
            "This is a checklist item.",
            "This is another checklist item.",
            "This is a third checklist item.",
        ]
    ),
    HorizontalRule(),
    CodeBlock("print('This is a code block.')", language="python"),
    Blockquote(["This is a blockquote.", Blockquote("This is a nested blockquote.")]),
    Footnotes(
        [
            "This is a footnote.",
            "This is another footnote.",
            "This is a third footnote.",
        ]
    ),
    DefinitionList(
        [
            (
                "This is a definition list item.",
                "This is a definition list item's definition.",
            ),
            (
                "This is another definition list item.",
                "This is another definition list item's definition.",
            ),
            (
                "This is a third definition list item.",
                "This is a third definition list item's definition.",
            ),
        ]
    ),
    Highlighting(
        [
            "This is a highlighted text.",
            "This is another highlighted text.",
            "This is a third highlighted text.",
        ]
    ),
]

print(dumps(document))
```
