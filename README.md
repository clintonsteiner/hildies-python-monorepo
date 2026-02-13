<h1 align="center">Hildie</h1>

<p align="center">
  <em>A Python monorepo built with Bazel, named after the best dog.</em>
</p>

<p align="center">
  <a href="https://pypi.org/project/hildie/"><img src="https://img.shields.io/pypi/v/hildie?color=blue" alt="PyPI"></a>
  <a href="https://pypi.org/project/hildie/"><img src="https://img.shields.io/badge/python-3.11%2B-blue" alt="Python 3.11+"></a>
  <a href="https://github.com/clintonsteiner/hildies-python-monorepo/actions"><img src="https://github.com/clintonsteiner/python-monorepo/actions/workflows/bazel.yml/badge.svg" alt="Build"></a>
  <a href="https://github.com/clintonsteiner/hildies-python-monorepo/blob/master/LICENSE"><img src="https://img.shields.io/badge/license-MIT-green" alt="License"></a>
</p>

---

## About

**Hildie** is a collection of Python utilities and tools, packaged as a single installable module. This project demonstrates a modern Python monorepo structure using [Bazel](https://bazel.build/) for builds, testing, and publishing.

Why "Hildie"? Because all the good package names were taken, so this project is named after Hildie — the adorable pup you see above, peacefully napping with her favorite stuffed horse.

## Installation

```bash
# Install main hildie package
pip install hildie

# Install hildie with optional Python bindings (Rust, Go, C++)
pip install hildie[bindings]
```

## Features

- **Modular Design**: Multiple sub-packages under a single namespace
- **Multi-Language**: Rust, Go, Node.js, Java, and C++ implementations
- **Python Bindings**: Use Rust, Go, and C++ directly from Python via PyO3 and ctypes
- **IPython/Jupyter Support**: Full support for interactive environments
- **Bazel Build System**: Fast, reproducible builds with caching
- **Automated Publishing**: Tag a release and it's automatically published to PyPI, npm, Maven, crates.io
- **Fully Tested**: Comprehensive test coverage across all packages and languages

## Packages

### Python Packages

| Package | Description |
|---------|-------------|
| `hildie.hildie_library` | Core utility functions for math operations |
| `hildie.hildie_app` | Application components for data processing |
| `hildie.hildie_cli` | Command-line interface tools |
| `hildie.hildie_archive_git_forks` | Utility for archiving GitHub forks |
| `hildie_bindings` | Python bindings for Rust, Go, and C++ (optional) |

### Other Languages

| Language | Package | Registry |
|----------|---------|----------|
| **Java** | hildie-java-lib | Maven Central |
| **Go** | hildie-go | pkg.go.dev |
| **Rust** | hildie-* | crates.io |
| **JavaScript** | @hildie/* | npm |
| **C++** | hildie-cpp | (native library) |

## Quick Start

### Basic Usage

```python
from hildie.hildie_library import add, multiply

# Simple math operations
result = add(2, 3)      # Returns: 5
product = multiply(4, 5) # Returns: 20
```

### Using the App

```python
from hildie.hildie_app import App

app = App()
result = app.process_numbers([1, 2, 3, 4, 5])
print(result)  # {'sum': 15, 'product': 120}
```

### CLI Tools

```bash
# After installing hildie
python -m hildie.hildie_cli --help
```

### GitHub Fork Archiver

```python
from hildie.hildie_archive_git_forks.archiver import GitHubForkArchiver

archiver = GitHubForkArchiver(token="your-github-token")
archiver.archive_forks("username")
```

### Python Bindings (Multi-Language)

With the `hildie[bindings]` extra, use Rust, Go, and C++ from Python:

```python
from hildie_bindings import (
    greet_rust, add_rust,              # Rust bindings (PyO3)
    greet_go, add_go,                   # Go bindings (ctypes)
    process_data, compute_factorial     # C++ bindings (ctypes)
)

# Use Rust functions
print(greet_rust("Hildie"))  # "Hello, Hildie!"
print(add_rust(5, 10))       # 15

# Use Go functions
print(greet_go("Gophers"))   # "Hello, Gophers!"
print(add_go(100, 200))      # 300

# Use C++ functions
print(process_data([1, 2, 3, 4, 5]))    # [2, 4, 6, 8, 10]
print(compute_factorial(5))              # 120
```

#### In IPython/Jupyter

Bindings work seamlessly in interactive environments:

```python
# In IPython or Jupyter - just import and use!
from hildie_bindings import greet_rust, add_rust

# Results displayed immediately
greet_rust("World")
add_rust(42, 8)
```

See [Interactive Demo](source/hildie/bindings/python/examples/Interactive_Demo.ipynb) for a complete Jupyter notebook.

## API Reference

### hildie.hildie_library

| Function | Description |
|----------|-------------|
| `add(a, b)` | Add two numbers together |
| `multiply(a, b)` | Multiply two numbers |

### hildie.hildie_app

| Class | Description |
|-------|-------------|
| `App` | Main application class for processing data |

### hildie.hildie_archive_git_forks

| Class | Description |
|-------|-------------|
| `GitHubForkArchiver` | Archive GitHub forks to local storage |

## Development

### Prerequisites

- [Bazelisk](https://github.com/bazelbuild/bazelisk) (recommended) or Bazel 7+
- Python 3.11+

### Building

```bash
# Build all targets
bazel build //...

# Build the wheel
bazel build //:wheel
```

### Testing

```bash
# Run all tests
bazel test //...
```

### Running CLIs

```bash
bazel run //:hildie-cli
bazel run //:hildie-archive-git-forks
```

## Project Structure

```
hildie/
├── source/
│   ├── hildie/                        # Multi-language source code
│   │   ├── java/                      # Java packages (Maven Central)
│   │   ├── go/                        # Go packages (pkg.go.dev)
│   │   ├── rust/                      # Rust crates (crates.io)
│   │   ├── node/                      # JavaScript/npm packages
│   │   ├── bindings/                  # Python bindings
│   │   │   └── python/                # PyO3 + ctypes bindings
│   │   │       ├── hildie_bindings/   # Package source
│   │   │       ├── examples/          # Demo scripts & notebooks
│   │   │       └── tests/             # Binding tests
│   │   └── cpp/                       # C++ components
│   └── python/                        # Python build tools
│       ├── build_bindings.py
│       ├── regenerate_requirements.py
│       ├── test_runners.py
│       └── hildie.bzl
├── docs/                              # Documentation
│   ├── *.md                           # All documentation files
│   ├── pyproject.toml
│   └── BUILD.bazel
├── packages/                          # Python package tests
│   ├── my-library/
│   ├── my-app/
│   ├── my-cli/
│   └── archive-git-forks/
├── BUILD.bazel                        # Root build file
├── MODULE.bazel                       # Bazel dependencies
├── pyproject.toml                     # Project metadata
└── README.md                          # This file
```

## Publishing

Releases are automated via GitHub Actions. To publish a new version:

```bash
git tag v0.2.0
git push origin v0.2.0
```

The workflow will:
1. Run all tests
2. Build the wheel with the tagged version
3. Publish to PyPI
4. Create a GitHub release

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Run tests (`bazel test //...`)
4. Commit your changes
5. Push to the branch
6. Open a Pull Request

## Maintainer

**Clinton Steiner** — [clintonsteiner@gmail.com](mailto:clintonsteiner@gmail.com)

- GitHub: [@clintonsteiner](https://github.com/clintonsteiner)

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  <em>Made by Clinton, inspired by Hildie</em>
</p>
<p align="center">
  <img src="https://raw.githubusercontent.com/clintonsteiner/hildies-python-monorepo/refs/heads/master/hildie.png" alt="Hildie the Dog" width="400"/>
</p>
