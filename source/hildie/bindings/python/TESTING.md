# Testing Hildie Python Bindings

This guide covers testing the Python bindings for Rust, Go, and C++ components.

## Test Files

### `tests/test_bindings.py`

Comprehensive test suite for all language bindings with:
- **TestRustBindings**: Tests for PyO3 Rust bindings
- **TestGoBindings**: Tests for ctypes Go bindings
- **TestCppBindings**: Tests for ctypes C++ bindings
- **TestCrossLanguageConsistency**: Cross-language validation
- **TestErrorHandling**: Edge cases and type handling

## Running Tests

### All Tests

```bash
# Using pytest directly
pytest src/hildie/bindings/python/tests/

# Using Bazel
bazel test //src/hildie/bindings/python/tests/

# With verbose output
pytest -v src/hildie/bindings/python/tests/
```

### Specific Test Class

```bash
# Test only Rust bindings
pytest src/hildie/bindings/python/tests/test_bindings.py::TestRustBindings -v

# Test only Go bindings
pytest src/hildie/bindings/python/tests/test_bindings.py::TestGoBindings -v

# Test only C++ bindings
pytest src/hildie/bindings/python/tests/test_bindings.py::TestCppBindings -v
```

### Specific Test

```bash
# Test single function
pytest src/hildie/bindings/python/tests/test_bindings.py::TestRustBindings::test_add_rust_basic -v
```

## Test Coverage

### Rust Bindings Tests

| Test | Purpose |
|------|---------|
| `test_greet_rust_basic` | Basic greeting functionality |
| `test_greet_rust_empty_name` | Edge case with empty string |
| `test_greet_rust_special_chars` | Unicode and special characters |
| `test_add_rust_basic` | Basic arithmetic |
| `test_add_rust_zero` | Addition with zero |
| `test_add_rust_negative` | Negative number handling |
| `test_add_rust_large_numbers` | Large number arithmetic |
| `test_greet_all_basic` | Multiple name greeting |
| `test_greet_all_single_name` | Single name with greet_all |
| `test_greet_all_empty` | Empty input handling |

### Go Bindings Tests

| Test | Purpose |
|------|---------|
| `test_greet_go_basic` | Basic greeting functionality |
| `test_greet_go_empty_name` | Edge case with empty string |
| `test_greet_go_special_chars` | Unicode and special characters |
| `test_add_go_basic` | Basic arithmetic |
| `test_add_go_zero` | Addition with zero |
| `test_add_go_negative` | Negative number handling |
| `test_add_go_large_numbers` | Large number arithmetic |

*Note: Go tests are skipped if bindings aren't compiled*

### C++ Bindings Tests

| Test | Purpose |
|------|---------|
| `test_process_data_basic` | Basic array multiplication |
| `test_process_data_empty` | Empty array handling |
| `test_process_data_single` | Single element array |
| `test_process_data_negative` | Negative number processing |
| `test_process_data_mixed` | Mixed positive/negative values |
| `test_process_data_large` | Large array processing |
| `test_compute_factorial_basic` | Basic factorial (5, 4, 3) |
| `test_compute_factorial_base_cases` | Base cases (0, 1, 2) |
| `test_compute_factorial_larger` | Larger factorials (6, 10) |
| `test_compute_factorial_sequence` | Sequential factorial values |

*Note: C++ tests are skipped if bindings aren't compiled*

### Cross-Language Tests

| Test | Purpose |
|------|---------|
| `test_add_consistency_rust_go` | Verify Rust and Go return same add results |
| `test_greet_consistency_rust_go` | Verify both greet functions handle names correctly |

### Error Handling Tests

| Test | Purpose |
|------|---------|
| `test_process_data_returns_list` | Return type validation |
| `test_process_data_list_length_preserved` | Data integrity |
| `test_greet_rust_returns_string` | String return type validation |
| `test_add_rust_returns_int` | Integer return type validation |

## Building Bindings Before Testing

### Build All Bindings

```bash
python3 tools/build_bindings.py --all
```

### Build Individual Bindings

```bash
# Build Rust bindings only
python3 tools/build_bindings.py --rust

# Build Go bindings only
python3 tools/build_bindings.py --go

# Build C++ bindings only
python3 tools/build_bindings.py --cpp
```

## Binding-Specific Requirements

### Rust (PyO3) Bindings

**Status**: Always available (native Python module)

**Build**:
```bash
cd src/hildie/bindings
maturin develop
```

### Go Bindings

**Status**: Optional (skipped if not compiled)

**Build**:
```bash
cd src/hildie/go
go build -o libhildie_go.so -buildmode=c-shared ./...
```

**Installation**:
```bash
cp libhildie_go.so src/hildie/bindings/python/hildie_bindings/lib/
```

### C++ Bindings

**Status**: Optional (skipped if not compiled)

**Build**:
```bash
g++ -shared -fPIC -std=c++17 -o libhildie_cpp.so src/hildie/cpp/hildie.cpp
```

**Installation**:
```bash
cp libhildie_cpp.so src/hildie/bindings/python/hildie_bindings/lib/
```

## Test Markers

Tests use pytest markers to handle optional bindings:

```python
@pytest.mark.skipif(not greet_go, reason="Go bindings not loaded")
def test_greet_go_basic(self):
    ...
```

**Behavior**:
- If bindings are loaded: Test runs normally
- If bindings are missing: Test is skipped with message
- Rust tests: Always run (PyO3 module)
- Go tests: Skipped if not compiled
- C++ tests: Skipped if not compiled

## Continuous Integration

### Testing Workflow

```yaml
# .github/workflows/bazel.yml
test:
  steps:
    - name: Build bindings
      run: python3 tools/build_bindings.py --all

    - name: Run binding tests
      run: pytest src/hildie/bindings/python/tests/ -v
```

## Troubleshooting

### Go Bindings Not Found

**Symptom**: Tests skipped with "Go bindings not loaded"

**Fix**:
```bash
python3 tools/build_bindings.py --go
```

### C++ Bindings Not Found

**Symptom**: Tests skipped with "C++ bindings not loaded"

**Fix**:
```bash
# Check if C++ compiler available
gcc --version  # or g++ --version

python3 tools/build_bindings.py --cpp
```

### Rust Bindings Missing

**Symptom**: ImportError when importing bindings

**Fix**:
```bash
# Rebuild with maturin
cd src/hildie/bindings
maturin develop
```

### Test Import Errors

**Symptom**: "No module named hildie_bindings"

**Fix**:
```bash
# Install the package in development mode
cd src/hildie/bindings/python
pip install -e .
```

## Testing Best Practices

1. **Build before testing**: Always run `python3 tools/build_bindings.py --all` first
2. **Check test output**: Look for skipped tests to identify missing bindings
3. **Run verbose tests**: Use `-v` flag to see detailed output
4. **Test cross-language consistency**: Verify same inputs yield consistent results

## Running Full Test Suite

```bash
# Build all bindings
python3 tools/build_bindings.py --all

# Run tests
pytest src/hildie/bindings/python/tests/ -v

# Or with Bazel
bazel test //src/hildie/bindings/python/tests:test_bindings
```

## Expected Test Results

### With All Bindings Compiled

```
========== test session starts ==========
collected 31 items

test_bindings.py::TestRustBindings::test_greet_rust_basic PASSED
test_bindings.py::TestRustBindings::test_add_rust_basic PASSED
...
test_bindings.py::TestCppBindings::test_compute_factorial_basic PASSED
...
========== 31 passed in 1.23s ==========
```

### Without Go Bindings

```
========== test session starts ==========
collected 31 items

test_bindings.py::TestRustBindings::test_greet_rust_basic PASSED
...
test_bindings.py::TestGoBindings::test_greet_go_basic SKIPPED (Go bindings not loaded)
...
========== 20 passed, 5 skipped in 1.15s ==========
```

## Further Reading

- [Python Bindings Guide](./BINDINGS_GUIDE.md)
- [Build Bindings Script](../../tools/build_bindings.py)
- [Hildie Namespaces](../../HILDIE_NAMESPACES.md)
