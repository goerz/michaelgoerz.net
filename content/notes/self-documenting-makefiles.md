---
Date: 2023-11-12
Category: Tech
Tags: make, python, julia
---

# Self-Documenting (GNU) Makefiles

[Makefiles](https://makefiletutorial.com) commonly contain ["phony" targets ("goals")](https://www.gnu.org/software/make/manual/html_node/Phony-Targets.html) that run some task. Typical examples include `make all`, `make test`, or `make clean`. It is a good idea to document all phony targets: running `make help` should print out a summary, resulting in a "self-documenting" Makefile. Ideally, `help` is the default target, so that just running `make` without any arguments prints the documentation.

To achieve this, a short description of each target should be included on the same line as the target, separated by ` ## `. For example:

```
.PHONY: help all clean test

.DEFAULT_GOAL := help

help:  ## Show this help
	@echo "N/A"

all:  ## Compile all binaries
	# TODO

clean:  ## Remove all compilation artifacts
	# TODO

test:  ## Run the tests
	# TODO
```

*All* phony targets should be listed in `.PHONY`. The `.DEFAULT_GOAL` should be set to `help` (and the `help` target should be the [first phony target](https://www.gnu.org/software/make/manual/html_node/Goals.html), just for good measure).

Now, we'll embed a small script in the Makefile so that the Makefile processes itself, finds all lines of the form `target:  ## description` and prints them in a nicely formatted table. This embedded script can be written in whatever language/tool is mostly likely to be available on the system. If the Makefile is for a Python project, it might be best to use a Python script.

The goal would be for `make` (or `make help`) to print

```
help                 Show this help
all                  Compile all binaries
clean                Remove all compilation artifacts
test                 Run the tests
```

Below are examples for how to achieve this with Python, Julia, and plain shell scripting.

## Python

```
.PHONY: help

.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
    match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
    if match:
        target, help = match.groups()
        print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

PYTHON ?= python3

help:   ## Show this help
	@$(PYTHON) -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)
```

The width of the padding (20) could be adjusted to the widths of the targets defined in the Makefile. Note that inside the `PRINT_HELP_PYSCRIPT`, lines are indented with 4 spaces (not tabs). However, the recipe for `help` (the line `@$(PYTHON) -c`…) must be indented with a single tab.



## Julia

```
.PHONY: help

.DEFAULT_GOAL := help

define PRINT_HELP_JLSCRIPT
rx = r"^([a-z0-9A-Z_-]+):.*?##[ ]+(.*)$$"
for line in eachline()
    m = match(rx, line)
    if !isnothing(m)
        target, help = m.captures
        println("$$(rpad(target, 20)) $$help")
    end
end
endef
export PRINT_HELP_JLSCRIPT

JULIA ?= julia

help:  ## Show this help
	@$(JULIA) -e "$$PRINT_HELP_JLSCRIPT" < $(MAKEFILE_LIST)
```

This is a direct translation of the above Python script.

## Shell

```
.PHONY: help

.DEFAULT_GOAL := help

define PRINT_HELP_PROLOGUE
This Makefile should work in most shell environments.

Running just `make` should be equivalent to `make help`

endef
export PRINT_HELP_PROLOGUE


help:  ## Show this help
	@echo "$$PRINT_HELP_PROLOGUE"
	@grep -E '^([a-zA-Z_-]+):.*## ' $(MAKEFILE_LIST) | awk -F ':.*## ' '{printf "%-20s %s\n", $$1, $$2}'
```

The above shell script version also includes a "prologue" of help text to be printed before the table of targets. Similar prologues (or epilogues) could also be included in the Python and Julia versions by adding appropriate print statements to the `PRINT_HELP_PYSCRIPT` or `PRINT_HELP_JLSCRIPT`.
