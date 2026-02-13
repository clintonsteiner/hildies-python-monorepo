# Hildie Monorepo Documentation

Welcome to Hildie, a multi-language monorepo built with Bazel.

## Quick Links

### Getting Started
- **[HILDIE_NAMESPACES.md](./HILDIE_NAMESPACES.md)** - Architecture & project structure
- **[TESTING.md](./TESTING.md)** - How to run tests
- **[GHA_BAZEL_BUILD.md](./GHA_BAZEL_BUILD.md)** - GitHub Actions workflow

### For Contributors
- **[PYTHON_BINDINGS.md](./PYTHON_BINDINGS.md)** - Python bindings architecture
- **[BINDINGS_TESTS_AND_EXAMPLES.md](./BINDINGS_TESTS_AND_EXAMPLES.md)** - Binding tests & examples
- **[CPP_EXAMPLES.md](./CPP_EXAMPLES.md)** - C++ compilation & examples

### Publishing & Configuration
- **[PUBLISHING_GUIDE.md](./PUBLISHING_GUIDE.md)** - Publishing to registries (PyPI, npm, Maven, crates.io)
- **[MAVEN_SETUP.md](./MAVEN_SETUP.md)** - Maven Central quick setup

## Project Structure

```
source/
├── hildie/           - Language implementations
│   ├── java/        - Java packages
│   ├── go/          - Go packages
│   ├── rust/        - Rust packages
│   ├── node/        - JavaScript/npm packages
│   ├── bindings/    - Python bindings
│   └── cpp/         - C++ components
└── python/          - Python tools & build scripts
```

## Key Commands

### Build & Test
```bash
# Build all
bazel build //source/hildie/...

# Test all
bazel test //...

# Run specific language tests
bazel test //source/hildie/java/...
bazel test //source/hildie/go/...
bazel test //source/hildie/rust/...
bazel test //source/hildie/node/...
```

### Python Bindings
```bash
# Build bindings
python3 source/python/build_bindings.py --all

# Test bindings
pytest source/hildie/bindings/python/tests/

# Run demo
python3 source/hildie/bindings/python/examples/bindings_demo.py
```

### Requirements
```bash
# Regenerate requirements from pyproject.toml
bazel build //:update_requirements
```

## Languages Supported

- **Python** - Main monorepo language
- **Java** - JARs published to Maven Central
- **Go** - Binaries, auto-published to pkg.go.dev
- **Rust** - Crates published to crates.io
- **JavaScript/TypeScript** - npm packages published to npm registry
- **C++** - Components with Python bindings

## Publishing

All packages are published via GitHub Actions on version tags (v*).

See [PUBLISHING_GUIDE.md](./PUBLISHING_GUIDE.md) for setup instructions.

## License

MIT License - See LICENSE file

---

For detailed information, see individual documentation files listed above.
