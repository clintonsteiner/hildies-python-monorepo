# Hildie Python Bindings

Python bindings for Hildie components written in Rust, Go, and C++.

## Quick Start

### Installation

```bash
# Build all bindings
python3 tools/build_bindings.py --all

# Install Python bindings package
cd src/hildie/bindings/python
pip install -e .
```

### Basic Usage

```python
from hildie_bindings import (
    # Rust (via PyO3)
    greet_rust,
    add_rust,
    greet_all,
    # Go (via ctypes)
    greet_go,
    add_go,
    # C++ (via ctypes)
    process_data,
    compute_factorial,
)

# Rust bindings
print(greet_rust("Alice"))  # "Hello, Alice!"
print(add_rust(2, 3))       # 5
print(greet_all("Alice", "Bob"))  # "Hello, Alice! Hello, Bob!"

# Go bindings
print(greet_go("Alice"))    # "Hello, Alice!"
print(add_go(2, 3))         # 5

# C++ bindings
print(process_data([1, 2, 3]))  # [2, 4, 6]
print(compute_factorial(5))     # 120
```

### Run Demo

```bash
# Run interactive demonstration
python3 src/hildie/bindings/python/examples/bindings_demo.py
```

### Run Tests

```bash
# Run all tests
pytest src/hildie/bindings/python/tests/ -v

# Run specific language tests
pytest src/hildie/bindings/python/tests/test_bindings.py::TestRustBindings -v
pytest src/hildie/bindings/python/tests/test_bindings.py::TestGoBindings -v
pytest src/hildie/bindings/python/tests/test_bindings.py::TestCppBindings -v
```

## Bindings Reference

### Rust Bindings (PyO3)

Native Python module compiled from Rust using PyO3. Always available after building.

#### `greet_rust(name: str) -> str`

Greet a person.

**Parameters**:
- `name` (str): Name to greet

**Returns**: str - Greeting message

**Example**:
```python
>>> from hildie_bindings import greet_rust
>>> greet_rust("Alice")
'Hello, Alice!'
```

#### `add_rust(a: int, b: int) -> int`

Add two integers.

**Parameters**:
- `a` (int): First number
- `b` (int): Second number

**Returns**: int - Sum of a and b

**Example**:
```python
>>> from hildie_bindings import add_rust
>>> add_rust(2, 3)
5
>>> add_rust(-5, 10)
5
```

#### `greet_all(*names: str) -> str`

Greet multiple people.

**Parameters**:
- `*names` (str): Variable number of names

**Returns**: str - Greeting message for all names

**Example**:
```python
>>> from hildie_bindings import greet_all
>>> greet_all("Alice", "Bob", "Charlie")
'Hello, Alice! Hello, Bob! Hello, Charlie!'
```

### Go Bindings (ctypes)

FFI bindings to compiled Go shared library using ctypes. Optional - tests skip if not compiled.

#### `greet_go(name: str) -> str`

Greet a person (Go implementation).

**Parameters**:
- `name` (str): Name to greet

**Returns**: str - Greeting message

**Requirements**:
- Go bindings compiled: `python3 tools/build_bindings.py --go`

**Example**:
```python
>>> from hildie_bindings import greet_go
>>> greet_go("Bob")
'Hello, Bob!'
```

#### `add_go(a: int, b: int) -> int`

Add two integers (Go implementation).

**Parameters**:
- `a` (int): First number
- `b` (int): Second number

**Returns**: int - Sum of a and b

**Requirements**:
- Go bindings compiled: `python3 tools/build_bindings.py --go`

**Example**:
```python
>>> from hildie_bindings import add_go
>>> add_go(10, 20)
30
```

### C++ Bindings (ctypes)

FFI bindings to compiled C++ shared library using ctypes. Optional - tests skip if not compiled.

#### `process_data(data: List[int]) -> List[int]`

Process integer array (multiply each element by 2).

**Parameters**:
- `data` (List[int]): List of integers to process

**Returns**: List[int] - Processed array

**Requirements**:
- C++ bindings compiled: `python3 tools/build_bindings.py --cpp`

**Example**:
```python
>>> from hildie_bindings import process_data
>>> process_data([1, 2, 3, 4, 5])
[2, 4, 6, 8, 10]
>>> process_data([-1, 0, 1])
[-2, 0, 2]
```

#### `compute_factorial(n: int) -> int`

Compute factorial of n.

**Parameters**:
- `n` (int): Number to compute factorial for

**Returns**: int - Factorial of n

**Requirements**:
- C++ bindings compiled: `python3 tools/build_bindings.py --cpp`

**Example**:
```python
>>> from hildie_bindings import compute_factorial
>>> compute_factorial(5)
120
>>> compute_factorial(0)
1
>>> compute_factorial(10)
3628800
```

## Architecture

### Rust Bindings

Uses **PyO3** - a framework for creating Python modules from Rust.

```
Rust code (src/hildie/rust/)
    ↓
PyO3 bindings (src/hildie/bindings/src/lib.rs)
    ↓
Native Python module (hildie_bindings.so)
    ↓
Python functions
```

**Features**:
- Native performance
- Automatic type conversion
- Memory-safe
- GIL handling built-in

### Go Bindings

Uses **ctypes** - Python's FFI for C libraries. Go functions are wrapped in C FFI.

```
Go code (src/hildie/go/)
    ↓
C-compatible wrapper
    ↓
Go shared library (libhildie_go.so)
    ↓
ctypes wrapper (hildie_bindings/go_bindings.py)
    ↓
Python functions
```

**Features**:
- Call compiled Go code from Python
- Automatic string encoding/decoding
- Integer type conversion

### C++ Bindings

Uses **ctypes** - Python's FFI for C libraries. C++ functions are exported as C.

```
C++ code (src/hildie/cpp/)
    ↓
C interface (hildie.h)
    ↓
C++ shared library (libhildie_cpp.so)
    ↓
ctypes wrapper (hildie_bindings/cpp_bindings.py)
    ↓
Python functions
```

**Features**:
- Call compiled C++ code from Python
- Array marshalling
- Manual memory management

## Building Bindings

### Build All

```bash
python3 tools/build_bindings.py --all
```

### Build Individual Bindings

```bash
# Rust (PyO3)
python3 tools/build_bindings.py --rust

# Go (ctypes)
python3 tools/build_bindings.py --go

# C++ (ctypes)
python3 tools/build_bindings.py --cpp
```

## System Requirements

### For Rust Bindings
- Python 3.11+ development headers
- Rust toolchain (cargo, rustc)
- maturin (Python build tool for Rust)

### For Go Bindings
- Go 1.21+ compiler
- C compiler (gcc or clang)
- C headers

### For C++ Bindings
- C++ compiler (g++ or clang++)
- Standard C++ library

## Installation Methods

### Method 1: Install with Main Hildie Package (Recommended)

```bash
# Install hildie with bindings support
pip install hildie[bindings]
```

This installs both the main hildie package and hildie-bindings together.

### Method 2: Direct Development Installation

```bash
cd source/hildie/bindings/python
pip install -e .
```

### Method 3: Build and Install Wheel

```bash
cd source/hildie/bindings/python
pip install build
python -m build
pip install dist/hildie_bindings-*.whl
```

### Method 4: Build Package (from source)

```bash
cd source/hildie/bindings/python
pip install build
python -m build --sdist
```

## IPython/Jupyter Usage

Hildie bindings work seamlessly in IPython and Jupyter notebooks!

### Interactive Demo in IPython

```python
# In IPython or Jupyter
from hildie_bindings import greet_rust, add_rust, process_data

# Use directly in interactive shell
greet_rust("IPython")          # Works instantly
result = add_rust(10, 20)      # Get results immediately
print(process_data([1, 2, 3])) # Process data interactively
```

### Using Jupyter Notebook

We provide an interactive notebook: `examples/Interactive_Demo.ipynb`

To run it:
```bash
jupyter notebook examples/Interactive_Demo.ipynb
```

### Python Demo Script

For non-Jupyter environments:
```bash
python3 examples/ipython_demo.py
```

## Testing

See [TESTING.md](./TESTING.md) for comprehensive testing guide.

### Quick Test

```bash
# Build bindings
python3 source/python/build_bindings.py --all

# Run tests
pytest source/hildie/bindings/python/tests/ -v
```

## Examples

### Basic Example

```python
from hildie_bindings import greet_rust, add_rust, process_data, compute_factorial

# Rust
name = "Alice"
greeting = greet_rust(name)
sum_result = add_rust(10, 20)

# C++
data = [1, 2, 3, 4, 5]
processed = process_data(data)
fact = compute_factorial(5)

print(f"{greeting}: {sum_result + sum(processed)}")
print(f"Factorial of 5: {fact}")
```

### Cross-Language Example

```python
from hildie_bindings import add_rust, add_go

# Both compute same result
a, b = 10, 20
rust_sum = add_rust(a, b)
go_sum = add_go(a, b)

assert rust_sum == go_sum
print(f"Consistent results: {rust_sum} == {go_sum}")
```

### Data Processing Example

```python
from hildie_bindings import process_data, compute_factorial

# Process array and compute factorial of size
data = [5, 10, 15, 20]
processed = process_data(data)
size_fact = compute_factorial(len(data))

print(f"Original: {data}")
print(f"Processed (×2): {processed}")
print(f"Factorial of size: {size_fact}")  # factorial(4) = 24
```

## Performance

Bindings provide near-native performance:

- **Rust**: Native performance (compiled directly)
- **Go**: Good performance (compiled C-compatible library)
- **C++**: Good performance (compiled C++ library)

Minimal overhead from ctypes marshalling for Go/C++.

## Error Handling

### Missing Bindings

If bindings aren't compiled, import warnings are issued:

```python
>>> from hildie_bindings import process_data
UserWarning: Hildie C++ bindings not found. Install with:
  cd src/hildie && g++ -shared -fPIC -o libhildie_cpp.so cpp/*.cpp
```

Calling functions raises ImportError:

```python
>>> process_data([1, 2, 3])
ImportError: C++ bindings not loaded. Please compile libhildie_cpp first.
```

### Type Conversion Errors

Type mismatches are handled gracefully:

```python
>>> add_rust("2", 3)  # String instead of int
TypeError: 'str' object cannot be interpreted as an integer
```

## Troubleshooting

### "Module not found: hildie_bindings"

**Solution**:
```bash
cd src/hildie/bindings/python
pip install -e .
```

### "Cannot find libhildie_go.so"

**Solution**:
```bash
python3 tools/build_bindings.py --go
```

### "Cannot find libhildie_cpp.so"

**Solution**:
```bash
python3 tools/build_bindings.py --cpp
```

### Tests show as "SKIPPED"

This is normal behavior. Optional bindings are skipped if not compiled:

```bash
# Build missing bindings
python3 tools/build_bindings.py --all

# Re-run tests
pytest src/hildie/bindings/python/tests/ -v
```

## License

MIT License - See LICENSE file

## Contributing

To add new bindings:

1. Add function to source language (Rust, Go, or C++)
2. Create ctypes/PyO3 wrapper
3. Add to `__init__.py`
4. Add tests in `tests/test_bindings.py`
5. Update this README

## See Also

- [TESTING.md](./TESTING.md) - Comprehensive testing guide
- [Hildie Namespaces](../../HILDIE_NAMESPACES.md) - Overall monorepo structure
- [Publishing Guide](../../PUBLISHING_GUIDE.md) - How to publish bindings
