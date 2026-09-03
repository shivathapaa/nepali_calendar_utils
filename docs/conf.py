"""Sphinx configuration for the nepali_calendar_utils API reference.

Docstrings are Google-style, so napoleon parses them directly. linkcode maps each
documented object back to the exact source lines on GitHub, mirroring the source
links produced by the sibling Kotlin library's Dokka site.
"""

import importlib
import inspect
import os
import sys

sys.path.insert(0, os.path.abspath("../src"))

project = "nepali_calendar_utils"
author = "Shiva Thapa"
copyright = "2024, Shiva Thapa"

try:
    from importlib.metadata import version as _dist_version

    release = _dist_version("nepali_calendar_utils")
except Exception:
    release = "3.0.0"
version = release

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx.ext.linkcode",
    "myst_parser",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "CODE_RULES.md"]

html_theme = "furo"
html_title = "nepali_calendar_utils"

add_module_names = False

autodoc_typehints = "description"
autodoc_member_order = "bysource"
autodoc_default_options = {
    "members": True,
    "show-inheritance": True,
}

napoleon_google_docstring = True
napoleon_numpy_docstring = False

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

# Resolve GitHub source links for documented objects. Anything that cannot be
# located (builtins, dynamically generated members) returns None, which simply
# omits the link rather than failing the build.
_repo_blob = "https://github.com/shivathapaa/nepali_calendar_utils/blob/main"
_pkg_file = inspect.getsourcefile(importlib.import_module("nepali_calendar_utils"))
_src_root = os.path.dirname(os.path.dirname(_pkg_file))
_repo_root = os.path.dirname(_src_root)


def linkcode_resolve(domain, info):
    if domain != "py" or not info.get("module"):
        return None

    try:
        obj = importlib.import_module(info["module"])
    except Exception:
        return None
    for part in info["fullname"].split("."):
        obj = getattr(obj, part, None)
        if obj is None:
            return None

    try:
        obj = inspect.unwrap(obj)
        source_file = inspect.getsourcefile(obj)
        lines, start = inspect.getsourcelines(obj)
    except (TypeError, OSError):
        return None
    if not source_file:
        return None

    rel = os.path.relpath(source_file, _repo_root)
    end = start + len(lines) - 1
    return f"{_repo_blob}/{rel}#L{start}-L{end}"
