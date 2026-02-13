# Python Bindings for Hildie Components

This guide explains how to build and use Python bindings for Rust, Go, and C++ components in Hildie.

## Overview

The bindings system provides a clean Python interface to high-performance native code:

- **Rust**: Via PyO3 (native Python extension module)
- **Go**: Via ctypes FFI (dynamic linking)
- **C++**: Via ctypes FFI (C interface)

## Structure

```
source/hildie/
├── bindings/                    # Python bindings (main package)
│   ├── Cargo.toml              # Rust project for PyO3 bindings
│   ├── pyproject.toml          # Python build configuration
│   ├── src/lib.rs              # Rust -> Python bindings
│   └── python/
│       └── hildie_bindings/    # Python package
│           ├── __init__.py     # Main module
│           ├── go_bindings.py  # Go FFI bindings
│           └── cpp_bindings.py # C++ FFI bindings
├── cpp/                         # C++ components
│   ├── hildie.h                # C++ header (C interface)
│   └── hildie.cpp              # C++ implementation
├── go/                          # Go library
│   ├── go.mod
│   └── lib/
├── rust/                        # Rust library
│   └── hildie-lib/
└── node/                        # Node.js library
```

## Quick Start

### Build All Bindings

```bash
# Build Rust bindings
cd source/hildie/bindings
maturin develop

# Build Go bindings
cd ../go
go build -o libhildie_go.so -buildmode=c-shared ./...

# Build C++ bindings
cd ../cpp
g++ -shared -fPIC -o libhildie_cpp.so hildie.cpp
```

### Or Use the Build Script

```bash
python3 tools/build_bindings.py
```

### Use in Python

```python
from hildie_bindings import (
    greet_rust,      # Rust binding
    add_rust,        # Rust binding
    greet_all,       # Rust binding
    greet_go,        # Go binding
    add_go,          # Go binding
    process_data,    # C++ binding
    compute_factorial  # C++ binding
)

# Rust examples
print(greet_rust("World"))           # "Hello from Hildie Rust Library, World!"
print(add_rust(2, 3))               # 5
print(greet_all(["Alice", "Bob"]))  # ["Hello...", "Hello..."]

# Go examples
print(greet_go("Gopher"))           # "Hello from Hildie Go Library, Gopher!"
print(add_go(10, 20))               # 30

# C++ examples
print(process_data([1, 2, 3]))      # [2, 4, 6]
print(compute_factorial(5))          # 120
```

## Detailed Setup

### 1. Rust Bindings (PyO3)

**Why PyO3?**
- ✅ Direct Python integration
- ✅ No overhead
- ✅ Pure Python package
- ✅ Type-safe at compile time

**Files:**
- `source/hildie/bindings/Cargo.toml` - Rust project
- `source/hildie/bindings/pyproject.toml` - Python metadata
- `source/hildie/bindings/src/lib.rs` - PyO3 bindings

**Build:**
```bash
cd source/hildie/bindings
pip install maturin
maturin develop          # For development
maturin build --release  # For distribution
```

**How it works:**
1. PyO3 macro converts Rust functions to Python callables
2. Type conversion happens automatically
3. Compiled to native extension module
4. Imports just like any Python module

**Example:**
```python
from hildie_bindings import greet_rust, add_rust

result = greet_rust("Alice")  # Rust function called from Python
sum_result = add_rust(5, 10)  # Returns Python int
```

### 2. Go Bindings (ctypes)

**Why ctypes?**
- ✅ No dependencies
- ✅ Works with existing Go code
- ✅ Dynamic linking
- ✅ Simple FFI

**Files:**
- `source/hildie/go/lib/` - Go source
- `source/hildie/bindings/python/hildie_bindings/go_bindings.py` - ctypes wrapper

**Build:**
```bash
cd source/hildie/go
go build -o libhildie_go.so -buildmode=c-shared ./...
# Copy to bindings location
cp libhildie_go.so ../bindings/python/hildie_bindings/lib/
```

**How it works:**
1. Go compiled as shared C library
2. ctypes loads .so/.dylib/.dll file
3. Define function signatures for ctypes
4. Call Go functions from Python
5. Handle data conversion (strings, ints, etc.)

**Example:**
```python
from hildie_bindings.go_bindings import greet_go

result = greet_go("Gopher")  # Calls Go function
```

### 3. C++ Bindings (ctypes)

**Why ctypes?**
- ✅ Works with existing C++ code
- ✅ C interface wrapper
- ✅ No C++ binding generator needed
- ✅ Maximum compatibility

**Files:**
- `source/hildie/cpp/hildie.h` - C interface header
- `source/hildie/cpp/hildie.cpp` - C++ implementation
- `source/hildie/bindings/python/hildie_bindings/cpp_bindings.py` - ctypes wrapper

**Build:**
```bash
cd source/hildie/cpp
g++ -shared -fPIC -o libhildie_cpp.so hildie.cpp
# Copy to bindings location
cp libhildie_cpp.so ../bindings/python/hildie_bindings/lib/
```

**How it works:**
1. C++ code wrapped with C interface
2. Compiled as shared library
3. ctypes loads library
4. Define C function signatures
5. Call C functions (which call C++ underneath)
6. Python handles memory management

**Example:**
```python
from hildie_bindings.cpp_bindings import compute_factorial

result = compute_factorial(5)  # Returns 120
```

## Build System Integration

### Bazel Build

```bazel
# In source/hildie/bindings/BUILD.bazel
filegroup(
    name = "rust_bindings",
    srcs = glob(["src/**/*.rs", "*.toml"]),
)

filegroup(
    name = "python_bindings",
    srcs = glob(["python/**/*.py"]),
)
```

### Or Manual Build

```bash
# One-command build
python3 tools/build_bindings.py --all

# Build specific component
python3 tools/build_bindings.py --rust
python3 tools/build_bindings.py --go
python3 tools/build_bindings.py --cpp
```

## Testing

```python
# Test all bindings
import hildie_bindings

# Rust
assert hildie_bindings.greet_rust("World") == "Hello from Hildie Rust Library, World!"
assert hildie_bindings.add_rust(2, 3) == 5

# Go
assert hildie_bindings.greet_go("Gopher") == "Hello from Hildie Go Library, Gopher!"
assert hildie_bindings.add_go(2, 3) == 5

# C++
assert hildie_bindings.process_data([1, 2, 3]) == [2, 4, 6]
assert hildie_bindings.compute_factorial(5) == 120

print("✅ All bindings working!")
```

## Performance

These bindings are designed for maximum performance:

| Component | Type | Overhead | Use Case |
|-----------|------|----------|----------|
| Rust (PyO3) | Native | Minimal | CPU-intensive, numerical |
| Go | ctypes | Low | Concurrent, I/O bound |
| C++ | ctypes | Low | Legacy code, system calls |

### Benchmarking

```python
import timeit
import hildie_bindings

# Rust
t = timeit.timeit(lambda: hildie_bindings.add_rust(1, 2), number=100000)
print(f"Rust: {t:.4f}s for 100k calls")

# Go
t = timeit.timeit(lambda: hildie_bindings.add_go(1, 2), number=100000)
print(f"Go: {t:.4f}s for 100k calls")
```

## Troubleshooting

### Library Not Found

```
ImportError: Hildie [language] bindings not found
```

**Solution:**
```bash
# Rebuild the component
python3 tools/build_bindings.py --[rust|go|cpp]
```

### Type Conversion Errors

```python
# Wrong type
result = greet_rust(123)  # Should be string

# Fix
result = greet_rust(str(123))
```

### Memory Issues with C++

```python
# Don't forget to free memory
data = process_data([1, 2, 3])  # C++ allocates memory
# Memory is automatically freed by Python
```

## Publishing Bindings

The bindings are published as part of the main `hildie` package:

```bash
# In package.json (Node.js)
npm install hildie

# In requirements.txt (Python)
pip install hildie-bindings

# In Cargo.toml (Rust - for Go/C++ bindings)
[dependencies]
hildie-bindings = "0.1.0"
```

## References

- [PyO3 Documentation](https://pyo3.rs/)
- [ctypes Tutorial](https://docs.python.org/3/library/ctypes.html)
- [Go cgo Documentation](https://pkg.go.dev/cmd/cgo)
- [C FFI Best Practices](https://nullprogram.com/blog/2018/12/29/)
