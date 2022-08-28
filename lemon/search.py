from .markdown import MarkdownType, Renderable


def contains(markdown: Renderable, obj: MarkdownType) -> bool:
    if isinstance(markdown, list):
        for item in markdown:
            if contains(item, obj):
                return True
    if obj in markdown:
        return True
    return False
