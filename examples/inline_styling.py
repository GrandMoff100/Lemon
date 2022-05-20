from lemon import Bold, Italics, Markdown, Strikethrough, dumps, loads

document = (
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

print(content := dumps(document))
# **My bold text** *is italisized* this is not ~~and also strikethrough~~ and more regular text **But bold again** ~~and then strikethrough~~ *and finally more italics.* finally some regular text.

print(loads(content))

# [
#     Markdown(
#         Bold('My bold text'),
#         Italics('is italisized'),
#         'this is not',
#         Strikethrough('and also strikethrough'),
#         'and more regular text',
#         Bold('But bold again'),
#         Strikethrough('and then strikethrough'),
#         Italics('and finally more italics.'),
#         'finally some regular text.'
#     )
# ]
