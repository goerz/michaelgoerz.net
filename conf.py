import hashlib
import re
import time
from pathlib import Path

from src.document import Tag, Category

AUTHOR = 'Dr. Michael Goerz'
SITENAME = 'Michael Goerz'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'US/Eastern'

PYGMENTS_STYLE = 'friendly'
# Scoped to dark mode, see the header of the CSS file
PYGMENTS_STYLE_DARK = 'github-dark'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

TYPOGRIFY = True

CC_LICENSE = "CC-BY-NC-SA"

MENUITEMS = (  # relative to SITEURL
    ("Research", ""),
    ("Programming", "programming/"),
    ("Studies", "studies/"),
    ("Refcards", "refcards/"),
    ("Notes", "notes/"),
)

DEFAULT_TEMPLATES = (
    (re.compile("^content/notes/.*"), "note.html"),
    (re.compile(".*"), "page.html")
)

# Social widget
SOCIAL = (
    ('fa-brands fa-mastodon', '@goerz@fosstodon.org', 'https://fosstodon.org/@goerz'),
    ('fa-brands fa-bluesky', 'bsky:michaelgoerz.net', 'https://bsky.app/profile/michaelgoerz.net'),
    ('fa-brands fa-square-github', 'GitHub', 'https://github.com/goerz'),
)

CONTACT = (
    ('fa-regular fa-envelope', 'mail@michaelgoerz.net', 'mailto:mail@michaelgoerz.net'),
    ('fa-solid fa-key', 'Public Keys', 'https://gist.github.com/goerz/81d58b19220026f8f5c1#public-sshgpg-keys'),
)

# The footer of every page except the Research page (which has a sidebar with
# all of CONTACT and SOCIAL) shows SOCIAL and only these contact links
FOOTER_CONTACT = CONTACT[:1]


REPO = "https://github.com/goerz/michaelgoerz.net"
HISTORY = f"{REPO}/commits/master"

SHOW_ARTICLE_CATEGORY = True
SHOW_DATE_MODIFIED = True

DIRECT_TEMPLATES = (('notes', 'tags', 'categories'))
NOTES_SAVE_AS = 'notes/index.html'

BIB_NAMES_TO_HIGHLIGHT = [
    "Michael H. Goerz",
]

CURRENT_TIME = time.ctime()

# Appended as `?v=` to theme asset URLs, so that browsers and the CDN fetch
# changed assets instead of serving stale cached copies
THEME_VERSION = hashlib.sha256(
    b"".join(
        f.read_bytes()
        for f in sorted(Path("theme/static").rglob("*"))
        if f.is_file() and f.name != ".DS_Store"
    )
).hexdigest()[:10]

Tag.URL = "tags.html#collapse-{slug}"
Category.URL = "categories.html#collapse-{slug}"


MATHJAX_SCRIPT = r"""
<script>
MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\(', '\\)']],
    displayMath: [['$$', '$$']]
  }
};
</script>
<script id="MathJax-script" defer
  src="https://cdn.jsdelivr.net/npm/mathjax@4/tex-chtml.js">
</script>
"""

REDIRECTS = []  # see conf_publish.py
