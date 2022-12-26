---
Date: 2015-12-18 17:45:03
Category: Programming
Tags: python, testing
---

# Using pytest Proto-Fixtures

The excellent [pytest][] framework uses the concept of [fixtures][] for
setup/teardown, and for sharing data between tests. However, fixtures can come
with a bit of “magic” the runs counter to Python’s tenet that [explicit is better
than implicit][pep20]. Specifically, built-in fixtures (or fixtures provided by
plugins) are used without being explicitly imported. Thus, a developer is likely
to be confused unless they are sufficiently familiar with the way pytest
works.

The situation is even graver when we want to share fixtures between multiple
test modules. The [recommended method for handling this][sharing] involves
defining the fixtures in a file `conftest.py` that is placed in the root of the
folder containing all the tests, and will be found and processed by pytest
automatically. Again, a developer must be aware of this behavior to figure out
where a fixture is coming from.

Sadly, there is no way to explicitly import fixtures into a testing module. What
we can do, however, is to define “proto-fixtures” as part of a project. A
proto-fixture is a routine that only needs to be decorated with `pytest.fixture`
to turn it into a fixture.

For example, there is a very nice fixture on [stackoverflow][datadir] that
defines a `datadir`: for every test module, we can have a folder with the exact
same name as the module, holding files that should be accessible to the test.
That is, with the following layout of files,

    .
    └── test
        ├── test_my_module
        │   ├── file1.dat
        │   └── file2.dat
        └── test_my_module.py

we can have a fixture `datadir` in `test_my_module.py` that would point to a
temporary copy of `./test/test_my_module`, including the files `file1.dat` and
`file2.dat`. This is clearly something we would want to have available in all of
our testing modules! So, we define the following routine in some module (let’s
say `testutils`):

```python
import os
from distutils import dir_util

def datadir(tmpdir, request):
    '''Proto-fixture responsible for searching a folder with the same name
    as a test module and, if available, moving all contents to a temporary
    directory so tests can use them freely.
    '''
    filename = request.module.__file__
    test_dir, _ = os.path.splitext(filename)

    if os.path.isdir(test_dir):
        dir_util.copy_tree(test_dir, str(tmpdir))

    return str(tmpdir)
```

Then, in `test_my_module.py`, and any other testing module, we could use this
in a very clear and explicit form, as:

```python
import testutil
import os
from pytest import fixture

datadir = pytest.fixture(testutil.datadir)

def test_my_function(datadir):
    assert os.path.isdir(datadir)
```


[pytest]: https://pytest.org
[fixtures]: https://pytest.org/latest/fixture.html
[datadir]: http://stackoverflow.com/questions/29627341/pytest-where-to-store-expected-data
[sharing]: https://pytest.org/latest/fixture.html#sharing-a-fixture-across-tests-in-a-module-or-class-session
[pep20]: https://www.python.org/dev/peps/pep-0020/

