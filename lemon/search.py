from typing import Type

from .markdown.markdown import Markdown, MarkdownType, Renderable


def contains(markdown: Renderable, obj: MarkdownType) -> bool:
    if isinstance(markdown, list):
        for item in markdown:
            if contains(item, obj):
                return True
    if isinstance(markdown, str):
        if isinstance(obj, str):
            if obj in markdown:
                return True
    if isinstance(markdown, (Markdown, list)):
        if obj in markdown:
            return True
    return False


# def find(markdown: Renderable, obj: Type[MarkdownType]) -> MarkdownType | None:
#     if isinstance(markdown, list):
#         for item in markdown:
#             if find(item, obj):
#                 return item
#     if isinstance(markdown, str):
#         if isinstance(obj, str):
#             if obj in markdown:
#                 return markdown
#     if isinstance(markdown, (Markdown, list)):
#         if obj in markdown:
#             return markdown
#     return None
