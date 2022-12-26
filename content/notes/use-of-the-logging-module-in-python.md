---
Date: 2015-08-16 10:06:54
Category: Programming
Tags: python, logging
---

# Use of the logging module in Python


## Logging in modules ##

In every module, import the logging module

```python
import logging
```

In every module routine, use the snippet

```python
logger = logging.getLogger(__name__)
```

Do not create a logger at module level.

In the routine, you may generate e.g. a debug message with

```python
logger.debug("This is a debug message")
```

## Logging in scripts – Configuring the root logger ##

Every script should configure the root level logger (e.g. in the main routine)

```python
logger = logging.getLogger()
logger.setLevel(logging.INFO)
```

See <http://victorlin.me/posts/2012/08/26/good-logging-practice-in-python>
for further configuration options.

Is is important that `getLogger` is called with no arguments, in order to obtain
the root logger. Any options set for the root logger are passed to all
loggers in the hierarchy.

Note that creating the logger explicitly is more robust than the alternative
method for configuring the root level logger through module methods, e.g.

```python
logging.basicConfig(level=logging.INFO)
```

This statement will have no effect if there are already any handlers set on the
root level logger.

## Logger hierarchy ##

Use the following routine to get a detailed overview of the logging hierarchy

```python
def show_loggers():
    loggers = [('root', logging.getLogger())]
    for name in sorted(logging.Logger.manager.loggerDict.keys()):
        logger = logging.getLogger(name)
        loggers.append( (name, logger) )
    for name, logger in loggers:
        indent = ""
        if name != 'root':
            indent = "   "*(name.count('.')+1)
        if logger.propagate:
            prop = "+ "
        else:
            prop = "  "
        handlers = ""
        if len(logger.handlers) > 0:
            handlers = ": " + str(logger.handlers)
        level = logging.getLevelName(logger.level)
        eff_level = logging.getLevelName(logger.getEffectiveLevel())
        if level == eff_level:
            level_str = ' [%s]' % level
        else:
            level_str = ' [%s -> %s]' % (level, eff_level)
        print indent + prop + name + level_str + handlers
```
