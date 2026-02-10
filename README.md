<p align="center">
  <img src="hildie.jpeg" alt="Hildie" width="400">
</p>

<h1 align="center">Hildie</h1>

<p align="center">
  <em>A Python monorepo built with Bazel, named after the best dog.</em>
</p>

<p align="center">
  <a href="https://pypi.org/project/hildie/"><img src="https://img.shields.io/pypi/v/hildie" alt="PyPI"></a>
  <a href="https://pypi.org/project/hildie/"><img src="https://img.shields.io/pypi/pyversions/hildie" alt="Python"></a>
  <a href="https://github.com/clintonsteiner/python-monorepo/actions"><img src="https://github.com/clintonsteiner/python-monorepo/actions/workflows/bazel.yml/badge.svg" alt="Build"></a>
</p>

---

## About

**Hildie** is a collection of Python utilities and tools, packaged as a single installable module. The project demonstrates a modern Python monorepo structure using Bazel for builds, testing, and publishing.

Named after Hildie the dog, because all the good package names were taken.

## Installation

```bash
pip install hildie
```

## Packages

| Package | Description |
|---------|-------------|
| `hildie.hildie_library` | Core utility functions |
| `hildie.hildie_app` | Application components |
| `hildie.hildie_cli` | Command-line interface tools |
| `hildie.hildie_archive_git_forks` | GitHub fork archiving utility |

## Usage

```python
from hildie.hildie_library import add, multiply

result = add(2, 3)  # 5
product = multiply(4, 5)  # 20
```

## Development

### Prerequisites

- [Bazelisk](https://github.com/bazelbuild/bazelisk) (recommended) or Bazel 7+
- Python 3.11+

### Commands

```bash
# Build everything
bazel build //...

# Run tests
bazel test //...

# Build wheel
bazel build //:wheel

# Run CLIs
bazel run //:hildie-cli
bazel run //:hildie-archive-git-forks
```

## Project Structure

```
├── src/hildie/                    # All source code
│   ├── hildie_library/            # Core library
│   ├── hildie_app/                # Application
│   ├── hildie_cli/                # CLI tool
│   └── hildie_archive_git_forks/  # Git fork archiver
├── packages/                      # Tests
├── tools/                         # Build macros
├── BUILD.bazel                    # Root build file
└── MODULE.bazel                   # Bazel module definition
```

## Publishing

Push a version tag to publish to PyPI:

```bash
git tag v0.2.0
git push origin v0.2.0
```

## Maintainer

**Clinton Steiner** - [clintonsteiner@gmail.com](mailto:clintonsteiner@gmail.com)

## License

MIT
