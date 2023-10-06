import re
import time

from src.document import Tag, Category

AUTHOR = 'Dr. Michael Goerz'
SITENAME = 'Michael Goerz'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'US/Eastern'

PYGMENTS_STYLE = 'friendly'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

TYPOGRIFY = True

CC_LICENSE = "CC-BY-NC-SA"

EXTERNALS = ()

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
    ('fa-globe', '@goerz@fosstodon.org', 'https://fosstodon.org/@goerz'),
    ('fa-github-square', 'Github', 'https://github.com/goerz'),
)

CONTACT = (
    ('fa-envelope-o', 'mail@michaelgoerz.net', 'mailto:mail@michaelgoerz.net'),
    ('fa-key', 'Public Keys', 'https://gist.github.com/goerz/81d58b19220026f8f5c1#public-sshgpg-keys'),
)


REPO = "https://github.com/goerz/michaelgoerz.net"
HISTORY = f"{REPO}/commits/master"

DISPLAY_TAGS_ON_SIDEBAR = False
SHOW_ARTICLE_CATEGORY = True
SHOW_DATE_MODIFIED = True

DIRECT_TEMPLATES = (('notes', 'tags', 'categories'))
NOTES_SAVE_AS = 'notes/index.html'

BIB_NAMES_TO_HIGHLIGHT = [
    "Michael H. Goerz",
]

CURRENT_TIME = time.ctime()

Tag.URL = "tags.html#collapse-{slug}"
Category.URL = "categories.html#collapse-{slug}"


MATHJAX_SCRIPT = r"""
<script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
<script>
MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\(', '\\)']],
    displayMath: [['$$', '$$']]
  }
};
</script>
<script type="text/javascript" id="MathJax-script" async
  src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml-full.js">
</script>
"""
# Combined components:
# - tex-chtml-full: OK in Chrome, baseline issue in Safari
# - tex-svg-full: OK in Chrome, pixellated in Safari

REDIRECTS = []  # see conf_publish.py
