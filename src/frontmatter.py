"""Process document frontmatter / metadata."""
import re
import datetime
import dateutil.parser

from .document import Tag, Category
from .get_history import get_history
from .logging import LOG


def read_date(date):
    """Convert the given date into `datetime.datetime`."""
    if isinstance(date, datetime.datetime):
        pass
    elif isinstance(date, datetime.date):
        date = datetime.datetime(*date.timetuple()[:6])
    elif isinstance(date, str):
        date = dateutil.parser.parse(date)
    else:
        raise ValueError(f"Cannot parse {date=}")
    return date


def sanitize_frontmatter(file, frontmatter):
    """Clean up and convert the given `frontmatter` dict for `file`."""
    frontmatter = {key.lower(): value for (key, value) in frontmatter.items()}
    history = get_history(file)
    frontmatter["history"] = history
    if "category" in frontmatter:
        category = frontmatter["category"]
        if not isinstance(category, Category):
            category = Category(category)
        frontmatter["category"] = category
    if "date" in frontmatter:
        try:
            frontmatter["date"] = read_date(frontmatter["date"])
        except ValueError:
            raise ValueError(f"Invalid date={frontmatter['date']} in {file=}")
    else:
        if len(history) > 0:
            LOG.debug("Obtained date for %s from git", file)
            date = history[0].date
        else:
            LOG.debug("No git history for %s: use now() as date", file)
            date = datetime.datetime.now()
        frontmatter["date"] = date
    if "revised" in frontmatter:
        try:
            frontmatter["revised"] = read_date(frontmatter["revised"])
        except ValueError:
            raise ValueError(
                f"Invalid revised={frontmatter['revised']} in {file=}"
            )
    if "tags" in frontmatter:
        tags = frontmatter["tags"]
        if isinstance(tags, str):
            tags = [Tag(tag) for tag in re.split(r",\s*", tags)]
        elif isinstance(tags, (list, tuple)):
            for (i, tag) in enumerate(tags):
                if not isinstance(tag, Tag):
                    tags[i] = Tag(tag)
        else:
            raise ValueError(f"Invalid {tag=} in {file=}")
        frontmatter["tags"] = tags
    else:
        frontmatter["tags"] = []
    return frontmatter
