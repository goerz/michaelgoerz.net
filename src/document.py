from .templates import slugify


class Document(dict):
    """Abstract representation of a document.

    This is simply a dict with attribute access. At a minimum, it must have
    keys `file`, `outfile`. In addition, it should have `content` and other
    meta-data used in the the template for rendering the file.

    Accessing non-existen attributes/keys returns None, which is convenient for
    templating.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "file" not in self:
            raise ValueError("Document must have source `file`")
        if "outfile" not in self:
            raise ValueError("Document must have `outfile`")

    def __getattr__(self, name):
        return self[name]

    def __setattr__(self, name, value):
        self[name] = value

    def __missing__(self, name):
        return None

    @property
    def up_to_date(self):
        return self.file.stat().st_mtime < self.outfile.stat().st_mtime


class Tag(str):
    """Wrapper around Tag string.

    Has a `url` property for use in templates, which can be enabled with e.g.

    ```
    Tag.URL = "tags.html#collapse-{slug}"
    ```
    """

    URL = None

    @property
    def slug(self):
        """Slugified tag name."""
        return slugify(self)

    @property
    def url(self):
        if self.URL is None:
            return None
        else:
            return self.URL.format(tag=self, slug=self.slug)


class Category(str):
    """Wrapper around Category string.

    Has a `url` property for use in templates, which can be enabled with e.g.

    ```
    Category.URL = "categories.html#collapse-{slug}"
    ```
    """

    URL = None

    @property
    def slug(self):
        """Slugified tag name."""
        return slugify(self)

    @property
    def url(self):
        if self.URL is None:
            return None
        else:
            return self.URL.format(tag=self, slug=self.slug)
