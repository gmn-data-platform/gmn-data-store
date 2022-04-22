"""Sphinx configuration."""
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.abspath("../src/gmn_data_store/"))

project = "GMN Data Store"
author = "Ricky Bassom"
copyright = f"{datetime.now().year}, {author}"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "autoapi.extension",
]
autodoc_typehints = "description"
html_theme = "furo"
autoapi_dirs = ["../src/gmn_data_store/"]
autoapi_add_toctree_entry = False
autoapi_generate_api_docs = True
autoapi_ignore = ["*__main__.py"]
autoapi_file_pattern = "*.py"
autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance",
    "special-members",
    "private-members",
    "show-module-summary",
    "show-module-summary",
    "special-members",
    "private-members",
    "show-module-summary",
]
autoapi_type = "python"
