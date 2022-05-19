from lemon import Bold, Header, Italics, Markdown, Strikethrough, Table, dumps, loads


class TestDumping:
    def test_Header(self) -> None:
        document = Header(
            "My Awesome Project",
            [
                "This project is so awesome that you should go star it on GitHub!",
                Header(
                    "Description", "You can implement nested sub-headers like magic!"
                ),
            ],
        )
        expected = (
            "# My Awesome Project\n\n"
            "This project is so awesome that you should go star it on GitHub!\n\n"
            "## Description\n\n"
            "You can implement nested sub-headers like magic!\n\n"
        )
        assert dumps(document) == expected

    def test_BoldItalicsStrikethrough(self) -> None:
        document = Markdown(
            Bold("My bold text"),
            Italics("is italisized"),
            "this is not",
            Strikethrough("and also strikethrough"),
            "and more regular text",
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
            "**But bold again** "
            "~~and then strikethrough~~ "
            "*and finally more italics.* "
            "finally some regular text."
        )

    def test_Table(self) -> None:
        data = Table(
            [
                ["Name", "Location", "Status"],
                ["Ted", "New York", "Busy"],
                ["Angie", "France", "Free"],
            ]
        )

        assert dumps(data) == (
            "|  Name  |  Location  |  Status  |\n"
            "|--------|------------|----------|\n"
            "|  Ted  |  New York  |  Busy  |\n"
            "|  Angie  |  France  |  Free  |\n"
        )


class TestLoading:
    def test_Header(self) -> None:
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
                    Markdown(
                        "This project is so awesome that you should go star it on GitHub!"
                    ),
                    Header(
                        "Description",
                        [Markdown("You can implement nested sub-headers like magic!")],
                    ),
                ],
            )
        ]

    def test_BoldItalicsStrikethrough(self) -> None:
        content = (
            "**My bold text** "
            "*is italisized* "
            "this is not "
            "~~and also strikethrough~~ "
            "and more regular text "
            "**But bold again** "
            "~~and then strikethrough~~ "
            "*and finally more italics.* "
            "finally some regular text. "
        )

        assert loads(content) == [
            Markdown(
                Bold("My bold text"),
                Italics("is italisized"),
                "this is not",
                Strikethrough("and also strikethrough"),
                "and more regular text",
                Bold("But bold again"),
                Strikethrough("and then strikethrough"),
                Italics("and finally more italics."),
                "finally some regular text.",
            )
        ]

    def test_Table(self) -> None:
        content = (
            "|  Name  |  Location  |  Status  |\n"
            "|--------|------------|----------|\n"
            "|  Ted  |  New York  |  Busy  |\n"
            "|  Angie  |  France  |  Free  |\n"
        )

        assert loads(content) == [
            Table(
                [
                    ["Name", "Location", "Status"],
                    ["Ted", "New York", "Busy"],
                    ["Angie", "France", "Free"],
                ]
            )
        ]
