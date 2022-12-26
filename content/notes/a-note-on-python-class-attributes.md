---
Date: 2015-12-10 20:20:27
Category: Programming
Tags: python, OOP
---

# A note on Python (class) attributes

Without an in-depth reading of the [Python Data Model][datamodel], there are a
few things about attributes in Python that might be surprising:

*   It is possible to add new attributes to any instances of “normal”
    user-defined classes after instantiation. This is because every class uses
    a `__dict__` under the hood for keeping track of attributes.

*   Assigning to an instance’s class attribute name does *not* set the value of
    the class attribute. Instead, it creates a new instance attribute with the
    same name, which shadows the class attribute

*   The only way (apart from things like C extension modules) to define a class
    that does not allow to create new attributes after instantiation is to use
    the [`__slots__` mechanism][slots]. This results in `__dict__` not being
    used.


Consider the following definition:

```python
class MyClass(object):
    a = 1 # class attribute
    def __init__(self):
        self.b = 1 # instance attribute

inst1 = MyClass()
inst2 = MyClass()
```


All instances share the same class attribute, so any changes in the attribute
value are reflected in all instances:

```python
>>> MyClass.a = 2
>>> inst1.a == inst2.a == 2
True
```

As a class attribute, `a` (in contrast to the instance attribute `b`) is not in
`inst1.__dict__`:

```python
>>> inst1.__dict__
{'b': 1}
```

An important feature of instance attributes is that new attributes can be
created not just in the `__init__` method, but even after the class is
instantiated. Needless to say, this just shows how important proper unit testing
is for Python development – a simple typo could end up creating a new attribute
instead of changing an existing attribute value.

```python
>>> inst1.new_attr = 0
>>> inst1.__dict__
{'b': 1, 'new_attr': 0}
```

This, combined with the way Python resolves attribute names, means that the
class attribute value can *not* be set as

```python
>>> inst1.a = 3
```

Instead of setting the class attribute value, this creates a new instance
attribute `a`:

```python
>>> inst1.a
3
>>> inst2.a
2
>>> inst1.__dict__
{'b': 1, 'new_attr': 0, 'a': 3}
```

It is even possible do delete the instance attribute again, “un-shadowing” the
class attribute:

```python
>>> inst1.a
3
>>> del inst1.a
>>> inst1.a
2
```

There is a [gist for a test][gist] that explores this more systematically, and
includes a comparison to classes defined with [`__slots__`][slots] (you should
not make a habit of needlessly preventing dynamic attribute creation with
`__slots__`!).

As a final note, it is recommended to access class attributes and instance
attributes in the same way whenever possible (i.e. `inst1.a` instead of
`inst1.__class__.a` or `MyClass.a` when working with the instance, and `self.a`
instead of `self.__class__.a` inside methods). This gives the flexibility to
[treat class attributes as defaults for instance attributes][classdef]

[datamodel]: https://docs.python.org/3.5/reference/datamodel.html#data-model
[classdef]: https://docs.python.org/2/reference/compound_stmts.html#class-definitions
[slots]: https://docs.python.org/3.5/reference/datamodel.html#slots
[gist]: https://gist.github.com/goerz/576f13e1a362bf5c6e3f

