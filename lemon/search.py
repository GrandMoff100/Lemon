from .markdown import Markdown, MarkdownType, Renderable


def contains(markdown: Renderable, obj: MarkdownType) -> bool:
    if isinstance(markdown, list):
        for item in markdown:
            if contains(item, obj):
                return True
    if isinstance(markdown, str):
        if isinstance(obj, str):
            if obj in markdown:
                return True
    if isinstance(markdown, list) or isinstance(markdown, Markdown):
        if obj in markdown:
            return True
    return False
