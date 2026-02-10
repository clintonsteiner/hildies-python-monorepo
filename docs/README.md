# Hildie Documentation

This directory contains the Sphinx documentation for the Hildie project.

## Building the Documentation

### Install Documentation Dependencies

```bash
# Using uv (recommended)
uv pip install -e ".[docs]"

# Or using pip
pip install -e ".[docs]"
```

### Build HTML Documentation

```bash
# From the docs directory
cd docs
make html

# View the documentation
open build/html/index.html
```

### Other Build Formats

```bash
make epub      # Build ePub version
make latexpdf  # Build PDF (requires LaTeX)
make linkcheck # Check all external links
make clean     # Clean build directory
```

## Documentation Structure

- `source/` - Documentation source files (reStructuredText)
- `source/conf.py` - Sphinx configuration
- `source/_static/` - Static files (images, CSS, etc.)
- `source/_templates/` - Custom templates
- `build/` - Generated documentation (git-ignored)

## Writing Documentation

Documentation is written in reStructuredText (RST) format. See the [Sphinx documentation](https://www.sphinx-doc.org/) for more information.

### Quick RST Reference

```rst
Section Header
==============

Subsection
----------

**bold** *italic* ``code``

- Bullet list
- Item 2

1. Numbered list
2. Item 2

.. code-block:: python

   def example():
       return "Hello, Hildie!"

.. note::
   This is a note box

.. warning::
   This is a warning box
```
