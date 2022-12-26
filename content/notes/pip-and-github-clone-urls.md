---
Date: 2015-02-12 16:16:40
Category: Tech
Tags: git, pip, python
---

# Pip and Github Clone URLs

Using the basic git protocol, as opposed to SSH or HTTPS is a reliable but
undocumented way of getting read-only access to Github repositories.


## Cloning a Github Repository ##

Github advertises two clone URLs for repositories: SSH and HTTPS. The usage, and
benefits of each is explained on the [Github help pages][1]. An undocumented
third option is to use the `git` protocol directly. For the repository
`goerz/mgplottools`, three equivalent possibilities are:

    git clone git@github.com:goerz/mgplottools.git
    git clone https://github.com/goerz/mgplottools.git
    git clone git://github.com/goerz/mgplottools.git

Note that the `.git` at the end of the url is optional. The SSH access is the
most convenient if you have SSH set up properly. HTTPS is the most flexible, and
the git protocol is for read-only access.

## Pip Installation from Github ##

For installing a Python package from a github repository, [`pip`][2] can be be
called with any of the three protocols:

    pip install git+ssh://git@github.com/goerz/mgplottools.git@master#egg=mgplottools
    pip install git+https://github.com/goerz/mgplottools.git@master#egg=mgplottools
    pip install git+git://github.com/goerz/mgplottools.git@master#egg=mgplottools

Again, `.git` can be omitted. Also the commit (`@master`) and package
information (`#egg=mgplottols`) can be omitted in certain circumstances, see the
[pip documentation][3].

When simply installing a package in this way, read-only access is the only thing
required. In principle, HTTPS *should* do the right thing, but I have observed
pip to prompt for a Github username and password when trying to clone a
repository that happens to be under your own Github account (i.e. where you have
read *and* write access). This can create significant problems when `pip
install` is called from an installation script, where no user-interaction is
possible. The "smart" HTTPS access is trying to be too smart for its own good in
this case.

Therefore, firewall-rules permitting,
**using `pip` in combination with the plain `git` protocol should be the
preferred method**
in installation scripts (or [IPython notebooks][4]).

[1]: https://help.github.com/articles/which-remote-url-should-i-use/
[2]: https://pip.pypa.io/en/latest/
[3]: https://pip.pypa.io/en/latest/reference/pip_install.html#git
[4]: http://ipython.org/notebook.html
