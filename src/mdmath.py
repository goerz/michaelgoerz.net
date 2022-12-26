"""MarkdownIt-Py plugin to protect math from markdown processing."""

import re
from functools import partialmethod

from markdown_it import MarkdownIt
from markdown_it.common.utils import escapeHtml
from markdown_it.common.utils import charCodeAt


def mdmath_plugin(md: MarkdownIt, delimiters="dollars"):
    """Plugin to recognized math."""

    if delimiters in RULES:
        for rule_inline in RULES[delimiters]["inline"]:
            md.inline.ruler.before(
                "escape", rule_inline["name"], make_inline_func(rule_inline)
            )

            _render_math_inline = partialmethod(
                render_math, tmpl=rule_inline["tmpl"]
            )
            md.add_render_rule(rule_inline["name"], _render_math_inline)

        for rule_block in RULES[delimiters]["block"]:
            md.block.ruler.before(
                "fence", rule_block["name"], make_block_func(rule_block)
            )

            _render_math_block = partialmethod(
                render_math, tmpl=rule_block["tmpl"]
            )
            md.add_render_rule(rule_block["name"], _render_math_block)
    else:
        raise ValueError(f"Unknown {delimiters=}")


def render_math(self, tokens, idx, options, env, *, tmpl):
    return tmpl.format(escapeHtml(tokens[idx].content))


def apply_rule(rule, string: str, begin, inBlockquote):

    if not (
        string.startswith(rule["tag"], begin)
        and (rule["pre"](string, begin) if "pre" in rule else True)
    ):
        return False

    match = rule["rex"].match(string[begin:])  # type: re.Match

    if not match or match.start() != 0:
        return False

    lastIndex = match.end() + begin - 1
    if "post" in rule:
        if not (
            rule["post"](string, lastIndex)  # valid post-condition
            and (not inBlockquote or "\n" not in match.group(1))
        ):
            return False
    return match


def make_inline_func(rule):
    def _func(state, silent):
        res = apply_rule(rule, state.src, state.pos, False)
        if res:
            if not silent:
                token = state.push(rule["name"], "math", 0)
                token.content = res[1]  # group 1 from regex ..
                token.markup = rule["tag"]

            state.pos += res.end()

        return bool(res)

    return _func


def make_block_func(rule):
    def _func(state, begLine, endLine, silent):
        begin = state.bMarks[begLine] + state.tShift[begLine]
        res = apply_rule(
            rule, state.src, begin, state.parentType == "blockquote"
        )
        if res:
            if not silent:
                token = state.push(rule["name"], "math", 0)
                token.block = True
                token.content = res[1]
                token.info = res[len(res.groups())]
                token.markup = rule["tag"]

            line = begLine
            endpos = begin + res.end() - 1

            while line < endLine:
                if (
                    endpos >= state.bMarks[line]
                    and endpos <= state.eMarks[line]
                ):
                    # line for end of block math found ...
                    state.line = line + 1
                    break
                line += 1

            state.pos = begin + res.end()

        return bool(res)

    return _func


def dollar_pre(str, beg):
    prv = charCodeAt(str[beg - 1], 0) if beg > 0 else False
    return (
        (not prv) or prv != 0x5C and (prv < 0x30 or prv > 0x39)  # no backslash,
    )  # no decimal digit .. before opening '$'


def dollar_post(string, end):
    try:
        nxt = string[end + 1] and charCodeAt(string[end + 1], 0)
    except IndexError:
        return True
    return (
        (not nxt) or (nxt < 0x30) or (nxt > 0x39)
    )  # no decimal digit .. after closing '$'


RULES: dict = {
    "dollars": {
        "inline": [
            {
                "name": "math_inline",
                "rex": re.compile(r"^\$(\S[^$]*?[^\s\\]{1}?)\$"),
                "tmpl": '<span class="math-inline">${0}$</span>',
                "tag": "$",
                "pre": dollar_pre,
                "post": dollar_post,
            },
        ],
        "block": [
            {
                "name": "math_block",
                "rex": re.compile(r"^\${2}([^$]*?)\${2}", re.M),
                "tmpl": '\n<div class="math-block">$${0}$$</div>\n',
                "tag": "$$",
            },
        ],
    },
}
