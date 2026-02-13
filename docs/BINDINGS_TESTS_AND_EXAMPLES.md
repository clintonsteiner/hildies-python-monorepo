# Hildie Python Bindings - Tests and Examples

Comprehensive test suite and examples for Python bindings to Rust, Go, and C++ components.

## Overview

This document indexes all test files and examples for the Hildie Python bindings system.

## Files Created

### Test Files

#### `source/hildie/bindings/python/tests/test_bindings.py`

**Comprehensive pytest test suite** with 31+ tests covering all bindings.

**Test Classes**:
- `TestRustBindings` (10 tests) - PyO3 Rust bindings
- `TestGoBindings` (7 tests) - ctypes Go bindings
- `TestCppBindings` (10 tests) - ctypes C++ bindings
- `TestCrossLanguageConsistency` (2 tests) - Cross-language validation
- `TestErrorHandling` (4 tests) - Edge cases and type handling

**Run Tests**:
```bash
pytest source/hildie/bindings/python/tests/test_bindings.py -v
```

**Key Features**:
- Rust: Always runs (PyO3 module)
- Go: Skipped if bindings not compiled
- C++: Skipped if bindings not compiled
- Parametrized tests for comprehensive coverage
- Cross-language consistency checks
- Error handling and edge cases

### Example Files

#### `source/hildie/bindings/python/examples/bindings_demo.py`

**Interactive demonstration script** showing all bindings in action.

**Demonstrations**:
1. Rust bindings (greet, add, greet_all)
2. Go bindings (greet, add)
3. C++ bindings (process_data, factorial)
4. Cross-language consistency
5. Error handling

**Run Demo**:
```bash
python3 source/hildie/bindings/python/examples/bindings_demo.py
```

**Output**: Comprehensive output showing all function calls and results

#### `source/hildie/cpp/example.cpp`

**C++ executable example** demonstrating library usage and Python integration.

**Examples**:
1. Basic data processing
2. Various input types (empty, single, negative, mixed)
3. Factorial computation
4. Large factorial values
5. Complex scenarios
6. Python usage patterns

**Compile**:
```bash
g++ -std=c++17 -o hildie_example source/hildie/cpp/example.cpp source/hildie/cpp/hildie.cpp
```

**Run**:
```bash
./hildie_example
```

### Documentation Files

#### `source/hildie/bindings/python/README.md`

**Comprehensive bindings reference** and getting started guide.

**Sections**:
- Quick Start
- Installation Methods
- Complete API Reference
- Architecture Overview
- Building Bindings
- System Requirements
- Testing
- Examples
- Performance Notes
- Error Handling
- Troubleshooting

**Use When**: Learning how to use the bindings

#### `source/hildie/bindings/python/TESTING.md`

**Testing guide** covering test structure, execution, and troubleshooting.

**Sections**:
- Test Files Overview
- Running Tests (all, specific class, specific test)
- Test Coverage Table
- Building Bindings
- Binding-Specific Requirements
- Test Markers
- CI/CD Integration
- Troubleshooting
- Best Practices
- Expected Results

**Use When**: Running or writing tests

#### `source/hildie/cpp/EXAMPLES.md`

**C++ examples and API documentation** with compilation and usage details.

**Sections**:
- Building the Example
- Expected Output
- Building Shared Library
- C++ API Reference
- Python Integration
- Performance Characteristics
- Compilation Flags
- Memory Management
- Troubleshooting
- Example Use Cases
- Extending with Functions

**Use When**: Working with C++ examples or building shared libraries

### Configuration Files

#### `source/hildie/bindings/python/BUILD.bazel`
Bazel configuration for Python bindings library.

#### `source/hildie/bindings/python/tests/BUILD.bazel`
Bazel configuration for test suite.

#### `source/hildie/bindings/python/setup.py`
Python setuptools configuration for installation.

#### `source/hildie/bindings/python/tests/__init__.py`
Python package marker for tests directory.

#### `source/hildie/bindings/python/examples/__init__.py`
Python package marker for examples directory.

## Quick Start

### 1. Build Bindings

```bash
# Build all bindings
python3 tools/build_bindings.py --all

# Or build individually
python3 tools/build_bindings.py --rust
python3 tools/build_bindings.py --go
python3 tools/build_bindings.py --cpp
```

### 2. Run Tests

```bash
# Install pytest if needed
pip install pytest

# Run all tests
pytest source/hildie/bindings/python/tests/test_bindings.py -v

# Run specific test class
pytest source/hildie/bindings/python/tests/test_bindings.py::TestRustBindings -v

# Run with Bazel
bazel test //source/hildie/bindings/python/tests:test_bindings
```

### 3. Run Examples

```bash
# Python demo
python3 source/hildie/bindings/python/examples/bindings_demo.py

# C++ example
g++ -std=c++17 -o hildie_example source/hildie/cpp/example.cpp source/hildie/cpp/hildie.cpp
./hildie_example
```

## Test Coverage

### Total Tests: 31+

| Category | Tests | Status |
|----------|-------|--------|
| Rust Bindings | 10 | Always run |
| Go Bindings | 7 | Conditional (compiled) |
| C++ Bindings | 10 | Conditional (compiled) |
| Cross-Language | 2 | Depends on availability |
| Error Handling | 4 | Always run |

### Test Types

| Type | Tests | Examples |
|------|-------|----------|
| Basic Functionality | 20 | add_rust, greet_go, process_data |
| Edge Cases | 5 | empty arrays, negative numbers, zero |
| Large Inputs | 3 | large arrays, large numbers |
| Type Conversion | 3 | return types, list preservation |
| Cross-Language | 2 | rust vs go, consistency checks |

## Bindings Summary

### Rust Bindings (PyO3)

**Functions**:
- `greet_rust(name: str) -> str`
- `add_rust(a: int, b: int) -> int`
- `greet_all(*names: str) -> str`

**Tests**: 10
**Status**: Always available

### Go Bindings (ctypes)

**Functions**:
- `greet_go(name: str) -> str`
- `add_go(a: int, b: int) -> int`

**Tests**: 7
**Status**: Skipped if not compiled

### C++ Bindings (ctypes)

**Functions**:
- `process_data(data: List[int]) -> List[int]`
- `compute_factorial(n: int) -> int`

**Tests**: 10
**Status**: Skipped if not compiled

## Directory Structure

```
source/hildie/
├── bindings/
│   └── python/
│       ├── hildie_bindings/          # Main package
│       │   ├── __init__.py           # Exports all bindings
│       │   ├── go_bindings.py        # Go ctypes wrapper
│       │   └── cpp_bindings.py       # C++ ctypes wrapper
│       ├── tests/
│       │   ├── __init__.py           # Package marker
│       │   ├── test_bindings.py      # Test suite (31+ tests)
│       │   └── BUILD.bazel           # Bazel config
│       ├── examples/
│       │   ├── __init__.py           # Package marker
│       │   └── bindings_demo.py      # Interactive demo
│       ├── README.md                 # Getting started guide
│       ├── TESTING.md                # Testing documentation
│       ├── setup.py                  # Installation config
│       └── BUILD.bazel               # Bazel config
├── cpp/
│   ├── hildie.h                      # C/C++ header
│   ├── hildie.cpp                    # C++ implementation
│   ├── example.cpp                   # C++ example with demos
│   └── EXAMPLES.md                   # Example documentation
└── ...

root/
└── BINDINGS_TESTS_AND_EXAMPLES.md    # This file
```

## Running Tests in Different Ways

### Pytest

```bash
# All tests
pytest source/hildie/bindings/python/tests/test_bindings.py -v

# With coverage
pytest source/hildie/bindings/python/tests/test_bindings.py --cov=hildie_bindings

# Verbose with detailed output
pytest source/hildie/bindings/python/tests/test_bindings.py -vv -s
```

### Bazel

```bash
# All tests
bazel test //source/hildie/bindings/python/tests:test_bindings

# With output
bazel test //source/hildie/bindings/python/tests:test_bindings --test_output=all
```

### Manual Python

```bash
cd source/hildie/bindings/python
python -m pytest tests/test_bindings.py -v
```

## Expected Output

### All Bindings Compiled

```
collected 31 items

TestRustBindings::test_greet_rust_basic PASSED
TestRustBindings::test_add_rust_basic PASSED
...
TestCppBindings::test_compute_factorial_basic PASSED
TestCrossLanguageConsistency::test_add_consistency_rust_go PASSED
...

============= 31 passed in 1.23s =============
```

### Some Bindings Missing

```
collected 31 items

TestRustBindings::test_greet_rust_basic PASSED
...
TestGoBindings::test_greet_go_basic SKIPPED (Go bindings not loaded)
TestCppBindings::test_process_data_basic SKIPPED (C++ bindings not loaded)
...

======= 20 passed, 5 skipped in 1.15s =======
```

## Development Guide

### Adding New Tests

1. Edit `tests/test_bindings.py`
2. Add test method to appropriate class
3. Use `@pytest.mark.skipif` for optional bindings
4. Run: `pytest tests/test_bindings.py::TestClass::test_name -v`

### Adding New Bindings

1. Implement function in source language (Rust/Go/C++)
2. Create wrapper in appropriate file (`go_bindings.py`, `cpp_bindings.py`, or Rust code)
3. Add to `__init__.py`
4. Add tests to `test_bindings.py`
5. Update `README.md`

### Extending Examples

1. Add function calls to `bindings_demo.py`
2. Add corresponding C++ code to `example.cpp`
3. Update `EXAMPLES.md` with new examples

## Troubleshooting

### Tests Skip Some Bindings

This is expected. Build missing bindings:
```bash
python3 tools/build_bindings.py --all
```

### Import Error

Install the package:
```bash
cd source/hildie/bindings/python
pip install -e .
```

### Compilation Error

Check system requirements:
- Rust: `rustc --version`
- Go: `go version`
- C++: `g++ --version`

## References

- [Python Bindings README](source/hildie/bindings/python/README.md)
- [Testing Guide](source/hildie/bindings/python/TESTING.md)
- [C++ Examples](source/hildie/cpp/EXAMPLES.md)
- [Hildie Namespaces](HILDIE_NAMESPACES.md)
- [Build Bindings Script](tools/build_bindings.py)

## License

MIT License - See LICENSE file

## Summary

This comprehensive test and example suite provides:

✅ **31+ tests** covering all bindings
✅ **Interactive demo** showing all features
✅ **C++ example** with compilation instructions
✅ **Complete documentation** with API references
✅ **Edge case handling** and error scenarios
✅ **Cross-language consistency** validation
✅ **Multiple ways** to run tests (pytest, Bazel, direct)

Perfect for developers learning to use the bindings or contributing new ones!
