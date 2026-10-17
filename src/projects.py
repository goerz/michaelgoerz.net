"""Render a YAML list of projects in Jinja templates.

See theme/templates/projects.html and content/programming/projects.yml
"""

import yaml


def read_yaml(filename):
    """Read a YAML file and return its data.

    This is intended as a Jinja function, but must be registered with
    `register_in_templates`.
    """
    with open(filename, encoding="utf-8") as yaml_file:
        return yaml.safe_load(yaml_file)


def register_in_templates(templates):
    """Register the required functions into the given template manager.

    The `templates` is an instances of `src.templates.Templates`.
    """
    templates.env.globals["read_yaml"] = read_yaml
