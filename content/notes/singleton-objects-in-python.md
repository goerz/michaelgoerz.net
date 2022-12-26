---
Date: 2016-11-09 16:40:56
Modified: 2017-03-12
Category: Programming
Tags: OOP, python
---

# Singleton Objects in Python

In Python 3, a [singleton][1] is best implemented as a metaclass
([see stackoverflow for a discussion of alternatives for implementing singlentons][2])

```python
class Singleton(type):
    """Metaclass for singletons. Any instantiation of a Singleton class yields
    the exact same object, e.g.:

    >>> class MyClass(metaclass=Singleton):
            pass
    >>> a = MyClass()
    >>> b = MyClass()
    >>> a is b
    True
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args,
                                                                **kwargs)
        return cls._instances[cls]

    @classmethod
    def __instancecheck__(mcs, instance):
        if instance.__class__ is mcs:
            return True
        else:
            return isinstance(instance.__class__, mcs)
```

In addition, we may want to be able to use the Singleton without explicitly
having to instantiate it. We can achieve this with a class decorator.

```python
def singleton_object(cls):
    """Class decorator that transforms (and replaces) a class definition (which
    must have a Singleton metaclass) with the actual singleton object. Ensures
    that the resulting object can still be "instantiated" (i.e., called),
    returning the same object. Also ensures the object can be pickled, is
    hashable, and has the correct string representation (the name of the
    singleton)
    """
    assert isinstance(cls, Singleton), \
        cls.__name__ + " must use Singleton metaclass"

    def self_instantiate(self):
        return self

    cls.__call__ = self_instantiate
    cls.__hash__ = lambda self: hash(cls)
    cls.__repr__ = lambda self: cls.__name__
    cls.__reduce__ = lambda self: cls.__name__
    obj = cls()
    obj.__name__ = cls.__name__
    return obj
```


We can now use this as

```python
@singleton_object
class MySingleton(metaclass=Singleton):
    pass
```

What the decorator does is to *replace* the `MySingleton` class with a singleton
object of the same name, so we can use `MySingleton` directly without having to
instantiate it (although the decorator ensures ``MySingleton is MySingleton()``
holds). We enforce that the object is properly hashable, its string
representation is its name, and that it can be pickled ([`__reduce__`][3]).

Lastly, we may define a dummy class that we can use to check whether objects are
singletons:

```python
class SingletonType(metaclass=Singleton):
    pass
```


This is used as

```python
>>> isinstance(MySingleton, SingletonType)
True
```


If [Sphinx autodoc][4] is used to generate documentation for a module containing
Singleton objects, a custom documenter will have to be registered. The Sphinx
`conf.py` file must contain the following:

```python
from sphinx.ext.autodoc import DataDocumenter

class SingletonDocumenter(DataDocumenter):
    directivetype = 'data'
    objtype = 'singleton'
    priority = 20
    @classmethod
    def can_document_member(cls, member, membername, isattr, parent):
        return isinstance(member, SingletonType)

def setup(app):
    # ... (other hook settings)
    app.add_autodocumenter(SingletonDocumenter)
```


[1]: https://en.wikipedia.org/wiki/Singleton_pattern
[2]: http://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
[3]: https://docs.python.org/3.5/library/pickle.html#object.__reduce__
[4]: http://www.sphinx-doc.org/en/stable/ext/autodoc.html
