.PHONY: help clean distclean venv black generate preview ipython install-kernel uninstall-kernel jupyter

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
    match = re.match(r'^([a-z0-9A-Z_-]+):.*?## (.*)$$', line)
    if match:
        target, help = match.groups()
        print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

PYTHON = .venv/bin/python

help:  ## Show this help
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)


venv: $(PYTHON)  ## Set up the virtual environment for building


black: $(PYTHON)  ## format Python source code with black
	$(PYTHON) -m black -l 80 generate.py src/*.py


clean:  ## Remove generated files
	rm -rf __pycache__
	rm -rf src/__pycache__
	rm -rf output


distclean: clean uninstall-kernel  ## Restore to a pristine checkout
	rm -rf content/notes/.ipynb_checkpoints
	rm -rf .venv


generate:  $(PYTHON)  ## Generate the website
	$< generate.py


preview:  $(PYTHON)  ## Generate and preview the website
	$< generate.py --preview


ipython: $(PYTHON)  ## Start an ipython interpreter
	$< -m IPython

install-kernel: $(PYTHON) ## Install Jupyter kernel into user environment
	$< -m pip install -r requirements-notebooks.txt
	$< -m ipykernel install --user --name michaelgoerz-net --display-name "michaelgoerz.net"

uninstall-kernel: ## Remove Jupyter kernel from user environment
	jupyter kernelspec remove -f michaelgoerz-net || true

jupyter: install-kernel  ## Start a Jupyter notebook server
	jupyter notebook

$(PYTHON):
	python3 -m venv .venv
	$(PYTHON) -m pip install --upgrade pip setuptools wheel
	$(PYTHON) -m pip install -r requirements.txt
