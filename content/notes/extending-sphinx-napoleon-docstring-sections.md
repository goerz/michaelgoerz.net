---
Date: 2015-12-30 16:36:27
Category: Programming
Tags: python, sphinx
---

# Extending Sphinx/Napoleon Docstring Sections

As explained in the [Napoleon manual][1], using low-level ReStructuredText
syntax in docstrings is a bad idea, as the docstrings will be effectively
unreadable in plain text (e.g. when interactively exploring a package in
IPython). Instead, [Google style docstrings][2] should be used, and rendered
using the [builtin Napoleon Sphinx extension][3]. In this style, the docstring
is organized using [sections][4]. There are only a small handful of
shortcomings:

*   The formatting of Attributes is less than ideal by default. It can be
    improved by setting `napoleon_use_ivar = True` in the [Sphinx `doc.py`][5],
    but this also causes the section to be named "Variables" instead of
    "Attributes"
*   It would be nice to distinguish (instance) attributes from class
    attributes, by allowing a "Class Attributes" section
*   When documenting classes that have a dictionary interface, it would be nice
    to have a "Keys" section

The source code for the Napoleon extension is written in such a way that makes
it easy to fix these annoyances. However, this would require forking the
extension. Instead, we may patch it at runtime to achieve the desired behavior.
Adding the following code in `doc.py` will achieve this:

```python
# -- Extensions to the  Napoleon GoogleDocstring class ---------------------

from sphinx.ext.napoleon.docstring import GoogleDocstring

# first, we define new methods for any new sections and add them to the class
def parse_keys_section(self, section):
    return self._format_fields('Keys', self._consume_fields())
GoogleDocstring._parse_keys_section = parse_keys_section

def parse_attributes_section(self, section):
    return self._format_fields('Attributes', self._consume_fields())
GoogleDocstring._parse_attributes_section = parse_attributes_section

def parse_class_attributes_section(self, section):
    return self._format_fields('Class Attributes', self._consume_fields())
GoogleDocstring._parse_class_attributes_section = parse_class_attributes_section

# we now patch the parse method to guarantee that the the above methods are
# assigned to the _section dict
def patched_parse(self):
    self._sections['keys'] = self._parse_keys_section
    self._sections['class attributes'] = self._parse_class_attributes_section
    self._unpatched_parse()
GoogleDocstring._unpatched_parse = GoogleDocstring._parse
GoogleDocstring._parse = patched_parse
```


[1]: http://sphinxcontrib-napoleon.readthedocs.org/
[2]: http://sphinxcontrib-napoleon.readthedocs.org/en/latest/example_google.html
[3]: http://sphinx-doc.org/ext/napoleon.html
[4]: https://pypi.python.org/pypi/sphinxcontrib-napoleon#sections
[5]: http://sphinx-doc.org/config.html#build-config
