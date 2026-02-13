# Configuration file for the Sphinx documentation builder.

import os
import sys
import tomllib
from pathlib import Path

# Add the project root to the path so autodoc can find the modules
sys.path.insert(0, os.path.abspath("../.."))
pyproject_file = Path(__file__).parent.parent.parent / "pyproject.toml"

# -- Project information -----------------------------------------------------
with open(pyproject_file, "rb") as f:
    project_metadata = tomllib.load(f)

# -- Project information -----------------------------------------------------
project = project_metadata["project"]["name"]
author = ", ".join([a["name"] for a in project_metadata["project"]["authors"]])

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
]

templates_path = ["_templates"]
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_logo = "_static/hildie.png"
html_favicon = "_static/hildie.png"

html_theme_options = {
    "logo_only": False,
    "display_version": True,
    "prev_next_buttons_location": "bottom",
    "style_external_links": False,
    "vcs_pageview_mode": "",
    "style_nav_header_background": "#2980B9",
    # Toc options
    "collapse_navigation": True,
    "sticky_navigation": True,
    "navigation_depth": 4,
    "includehidden": True,
    "titles_only": False,
}

html_context = {
    "display_github": True,  # Integrate GitHub
    "github_user": "clintonsteiner",  # Username
    "github_repo": "hildies-python-monorepo",  # Repo name
    "github_version": "master",  # Version
}

# -- Intersphinx configuration -----------------------------------------------
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}
