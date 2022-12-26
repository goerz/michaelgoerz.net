---
Date: 2018-12-26 15:43:55
Category: Programming
Tags: documentation, git, pip, python
---

# Inter-Release Versioning Recommendations

I've always been a bit confused as to what version to set in the source
code of software packages *between* releases. For Python packages, this is the
string in the `__version__` attribute of the package.
After an in-depth reading of [PEP 440][] and the [Semantic Versioning][]
specification, I've come to the conclusion that the correct approach is to
**either use the version number of the last release, with "+dev" appended, or
the version number of the next planned release, with "-dev" appended.**

## Release Versioning

[Semantic Versioning][] and [PEP 440][] give relatively straightforward
recommendations for the version numbers of *releases*:

*   Normal releases follow the pattern `<major>.<minor>.<patch>`.

*   The initial release of a project is `0.1.0`.

*   The initial *stable* release of a project is `1.0.0`.

*   A package may publish pre-releases. I recommend following
    [Semantic Versioning][], and to append the pre-release identifier with a
    dash, e.g.

    ```shell
    1.0.0-dev1  # developer's preview 1 for release 1.0.0
    1.0.0-rc1   # release candidate 1 for 1.0.0
    ```

    I use "developer's previews" primarily when another project (like a
    research paper) depends on an unstable current state of a package, and
    I want to mark this relationship with something more permanent than a reference
    to a specific commit. [PEP 440] also allows "alpha" and "beta" releases prior
    to release candidates, but this is not something I would generally consider
    for a smallish package. In any case, [setuptools][] (and [pip][]) orders
    these releases correctly:

    ```pycon
    >>> from pkg_resources import parse_version  # pkg_resources is part of setuptools
    >>> (parse_version('1.0.0-dev1')
    ...  < parse_version('1.0.0-dev2')
    ...  < parse_version('1.0.0-a1')
    ...  < parse_version('1.0.0-b1')
    ...  < parse_version('1.0.0-rc1')
    ...  < parse_version('1.0.0-rc2')
    ...  < parse_version('1.0.0'))
    True
    ```

*   A package may also publish post-releases, for correcting errors in the
    release meta-data or documentation only. These look as e.g.

    ```shell
    1.0.0.post1  # first post-release after 1.0.0
    ```

    and are ordered correctly:

    ```pycon
    >>> parse_version('1.0.0') < parse_version('1.0.0.post1')
    True
    ```

The recommendation to separate pre-release specifiers with dashes in
[Semantic Versioning][] violates a strict [PEP 440][]. That is, the dashed form
cannot be used when uploading a package to [PyPI][]. Luckily, [twine][] will
correctly normalize e.g. `1.0.0-dev1` into the canonical `1.0.0dev1` that
[PyPI][] will accept. Also, [pip][] and similar tools perform the same
normalization: A package can be installed using *any* variation of the version
string, as long as it normalizes to the same canonical result. Thus, there is
no problem with e.g.  `1.0.0-dev1` in practice, and I recommend using it for
the `__version__` string, and when tagging the release in git (tag name
`v1.0.0-dev1`). If you prefer to user the canonical [PEP 440][] form of
pre-releases without a dash, in violation of [Semantic Versioning][], you
should feel free to do so, as long as releases within a project are
consistent. Note also that [Semantic Versioning][] strictly speaking does not
allow post-releases. These should be used sparingly anyway, and only ever for
fixing meta-data, such as a broken description on [PyPI][].

## Development Versioning

Between releases, [PEP 440][] and [Semantic Versioning][] requirements
technically do not apply to `__version__`. Traditionally, I've usually left
`__version__` unchanged between releases, or sometimes set it to the version
number of an upcoming release. The problem with this is that it is not at all
uncommon for a Python package to be installed "from master" (especially during
development, or for "in-house" use). [Pip directly supports this][1]. Then, one
example where the `__version__` becomes visible is when using the [watermark][]
extension for printing the versions of imported packages in [Jupyter
notebooks][]. For reproducibility, the information whether a released version
of a package or a development version from an arbitrary git commit is used is
highly relevant.  With a "development installation", inspecting `__version__`
does not allow to detect that the installed version is not a release, and
moreover, it is unclear whether the code is in a state *before* the specified
`__version__`, or *after*.

A good solution is to append "+dev" to `__version__` on the master (release)
branch immediately after a release is published. Alternatively, if the next
version to be released from a branch is known with certainty, `__version__` can
be set to that upcoming release with "-dev" appended.

From a technical perspective, "+dev" is a ["local version identifier"][2]
according to [PEP 440][], and ["build metadata"][3] according to
[Semantic Versioning][]. The "-dev" suffix is a [pre-release version][4] in
either specification. We are stretching these definitions just slightly:
[Semantic Versioning][3] says that local version identifiers ("+dev") should be
ignored when determining version precedence. However, [setuptools][] orders
"+dev" and "-dev" in the "correct" way:

```pycon
>>> parse_version('1.0.0') < parse_version('1.0.0+dev')
True
>>> parse_version('1.0.0-dev') < parse_version('1.0.0')
True
```

While it takes some getting used to, putting "1.0.0-dev1+dev" in `__version__`
after having released developer's preview `1.0.0-dev1` is perfectly fine, and
preferable to "1.0.0-dev" unless you are certain that there will be no more
dev/rc releases before the normal `1.0.0` release.

```pycon
>>> parse_version('1.0.0-dev1') < parse_version('1.0.0-dev1+dev')
True
>>> parse_version('1.0.0-dev1+dev') < parse_version('1.0.0')
True
```

Even "1.0.0-dev1-dev" is technically OK to indicate commits leading up to
`1.0.0-dev1`, although I would avoid this, personally. Generally, on a given
branch, the `__version__` string should only ever move forward (according to
`parse_version`).

Even more important than [setuptools][] ordering the local `__version__`
correctly relative to releases is that the "+dev" and "-dev" suffixes
read very intuitively to humans: "1.0.0+dev" is the code from release `1.0.0`
plus some additional development, and "1.0.0-dev" is the code from release
`1.0.0` minus some missing pieces. Note that the "+dev" and "-dev" will never
make it into a released version on [PyPI][].

The system should also be flexible enough for arbitrary branching models. In my
own projects, I usually have a very simple model with only `master` and
topic-branches (with a release being a tag on `master`). Since I don't usually
know which version will be released next, I will keep the "+dev" suffix between
releases. For a more involved branching model, e.g. [git-flow][] with its
release and hotfix branches, it may be clear which release will be made next
from a particular branch, and then the "-dev" suffix would be more appropriate.

## Regex for allowed version strings

The above recommendations can be summarized in `__version__` having to match
the following regex at all times:

```pycon
>>> import re
>>> RX_VERSION = re.compile(
...    r'^(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)'
...    r'(?P<prepost>\.post\d+|-(dev|a|b|rc)\d+)?'
...    r'(?P<devsuffix>[+-]dev)?$'
... )
```

For a *released* version, the `devsuffix` group must be empty.

While these recommendations apply to Python packages in particular, I would
also advocate them for software projects in general, assuming they don't clash
substantially with existing conventions.


[PEP 440]: https://www.python.org/dev/peps/pep-0440/
[Semantic Versioning]: https://semver.org
[setuptools]: https://setuptools.readthedocs.io/en/latest/
[pip]: https://pip.readthedocs.io/en/stable/
[PyPI]: https://pypi.org
[twine]: https://twine.readthedocs.io/en/latest/
[watermark]: https://github.com/rasbt/watermark
[git-flow]: https://nvie.com/posts/a-successful-git-branching-model/
[Jupyter notebooks]: https://jupyter.org
[1]: https://michaelgoerz.net/notes/pip-and-github-clone-urls.html#pip-installation-from-github
[2]: https://www.python.org/dev/peps/pep-0440/#local-version-identifiers
[3]: https://semver.org/#spec-item-10
[4]: https://semver.org/#spec-item-9
