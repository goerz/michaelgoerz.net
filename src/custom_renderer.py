from markdown_it.renderer import RendererHTML
from markdown_it.token import Token
from markdown_it.common.utils import escapeHtml, unescapeAll


class CustomRenderer(RendererHTML):
    """Custom renderer (for render_markdown).

    This fixes problems with nested <pre> tags.
    """

    __output__ = "html"

    def code_block(
        self,
        tokens,
        idx,
        options,
        env,
    ):
        """Handle indented code blocks."""
        return "<pre>" + escapeHtml(tokens[idx].content) + "</pre>\n"

    def fence(
        self,
        tokens,
        idx,
        options,
        env,
    ):
        """Handle fenced code blocks."""
        token = tokens[idx]
        info = unescapeAll(token.info).strip() if token.info else ""
        langName = ""
        langAttrs = ""

        if info:
            arr = info.split(maxsplit=1)
            langName = arr[0]
            if len(arr) == 2:
                langAttrs = arr[1]

        if options.highlight:
            highlighted = options.highlight(
                token.content, langName, langAttrs
            ) or escapeHtml(token.content)
        else:
            highlighted = escapeHtml(token.content)

        return highlighted + "\n"
