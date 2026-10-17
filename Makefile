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

help:  ## Show this help
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)


venv:  ## Set up the virtual environment for building
	uv sync


black:  ## format Python source code with black
	uv run black -l 80 generate.py src/*.py


clean:  ## Remove generated files
	rm -rf __pycache__
	rm -rf src/__pycache__
	rm -rf output


distclean: clean uninstall-kernel  ## Restore to a pristine checkout
	rm -rf content/notes/.ipynb_checkpoints
	rm -rf .venv


generate:  ## Generate the website
	uv run python generate.py


preview:  ## Generate and preview the website
	uv run python generate.py --preview


ipython:  ## Start an ipython interpreter
	uv run ipython

install-kernel:  ## Install Jupyter kernel into user environment
	uv run python -m ipykernel install --user --name michaelgoerz-net --display-name "michaelgoerz.net"

uninstall-kernel: ## Remove Jupyter kernel from user environment
	jupyter kernelspec remove -f michaelgoerz-net || true

jupyter: install-kernel  ## Start a Jupyter notebook server
	jupyter notebook
