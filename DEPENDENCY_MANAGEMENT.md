# Dependency Management

This project uses `pyproject.toml` as the single source of truth for Python dependencies, with Bazel for builds.

## Overview

- **Source of truth**: `pyproject.toml` (not requirements.txt)
- **Lock files**: Generated using `uv pip compile`
- **Build tool**: Bazel with `rules_python`

## Dependency Types

### Main Dependencies
Defined in `pyproject.toml`:
```toml
[project]
dependencies = [
    "click",
    "requests",
]
```

### Optional Dependencies
```toml
[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-cov>=4.1.0",
    "ruff>=0.15.0",
]
docs = [
    "sphinx>=9.0.4",
    "sphinx-rtd-theme>=3.0.0",
    "sphinxcontrib-jquery",
    "roman",
]
```

## Workflow

### Adding a New Dependency

1. **Add to pyproject.toml**:
   ```toml
   [project]
   dependencies = [
       "click",
       "requests",
       "new-package>=1.0.0",  # Add here
   ]
   ```

2. **Regenerate lock file**:
   ```bash
   # For main + dev dependencies
   uv pip compile pyproject.toml --extra dev -o requirements_lock.txt

   # For docs dependencies
   uv pip compile pyproject.toml --extra docs -o requirements_docs_lock.txt
   ```

3. **Bazel will automatically pick up the changes** on next build.

### Installing Dependencies Locally

```bash
# Install main dependencies
uv pip install -e .

# Install with dev tools
uv pip install -e ".[dev]"

# Install with docs tools
uv pip install -e ".[docs]"

# Install everything
uv pip install -e ".[dev,docs]"
```

## Lock Files

Lock files are generated from `pyproject.toml` and tracked in git:

- `requirements_lock.txt` - Main + dev dependencies
- `requirements_docs_lock.txt` - Docs dependencies

**Never edit lock files directly!** Always regenerate them from `pyproject.toml`.

## Bazel Integration

The `MODULE.bazel` file references the lock files:

```python
pip.parse(
    hub_name = "pip",
    python_version = "3.12",
    requirements_lock = "//:requirements_lock.txt",
)
pip.parse(
    hub_name = "pip_docs",
    python_version = "3.12",
    requirements_lock = "//:requirements_docs_lock.txt",
)
```

## Common Tasks

### Update All Dependencies
```bash
# Regenerate all lock files with latest compatible versions
uv pip compile pyproject.toml --extra dev -o requirements_lock.txt --upgrade
uv pip compile pyproject.toml --extra docs -o requirements_docs_lock.txt --upgrade
```

### Check for Outdated Dependencies
```bash
uv pip list --outdated
```

### Build and Test
```bash
# Build
bazel build //...

# Test
bazel test //...
```

## Why This Approach?

✅ **Single source of truth**: All dependencies in `pyproject.toml`
✅ **No manual requirements.txt**: Lock files auto-generated
✅ **Standard Python tooling**: Uses PEP 621 standards
✅ **Fast with uv**: `uv` is much faster than pip-tools
✅ **Bazel compatible**: Lock files work with rules_python
✅ **Reproducible builds**: Lock files ensure consistent dependencies
