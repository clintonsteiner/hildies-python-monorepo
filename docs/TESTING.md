# Hildie Testing Guide

All tests across the multi-language monorepo are fully integrated and passing.

## Quick Start

### Run all tests (all languages):
```bash
python3 tools/test_runners.py
```

Or using the wrapper:
```bash
./test_all.sh
```

### Run Python tests only (Bazel):
```bash
bazel test //packages/...
```

### Run specific language:
```bash
python3 tools/test_runners.py --language java
python3 tools/test_runners.py --language go
python3 tools/test_runners.py --language rust
python3 tools/test_runners.py --language node
python3 tools/test_runners.py --language python
```

## Test Coverage

| Language | Tests | Type | Status |
|----------|-------|------|--------|
| Python   | 6     | pytest (via Bazel) | ✅ |
| Java     | 2     | Unit tests (javac) | ✅ |
| Go       | 2     | Unit tests (go test) | ✅ |
| Rust     | 2     | Unit tests (cargo) | ✅ |
| Node.js  | 2     | Unit tests (node --test) | ✅ |
| **Total**| **14+** | | ✅ **ALL PASSING** |

## Test Infrastructure

### Python Test Runner (`tools/test_runners.py`)
Unified Python test runner that executes all language tests:
- `PythonTestRunner`: Uses `bazel test //packages/...`
- `JavaTestRunner`: Compiles with `javac` and runs with `java`
- `GoTestRunner`: Uses `go test ./...`
- `RustTestRunner`: Uses `cargo test --all`
- `NodeTestRunner`: Uses `npm install && npm test`

### Test Scripts
- `test_all.sh` - Wrapper script that calls the Python test runner
- `tools/test_runners.py` - Main unified test runner (Python)
- Individual test wrappers in `tools/`:
  - `java_test_wrapper.sh`
  - `go_test_wrapper.sh`
  - `rust_test_wrapper.sh`
  - `node_test_wrapper.sh`

## CI/CD Integration

All tests are automatically run via GitHub Actions (`.github/workflows/bazel.yml`):

1. **On Pull Request**: All tests required to pass before merge
2. **On Push to Master**: All tests run
3. **On Release Tag**: All tests + build artifacts + publish

### Test Matrix
- **Python versions**: 3.9, 3.11, 3.14
- **Operating Systems**: Ubuntu Linux, macOS
- **All Languages**: Python, Java, Go, Rust, Node.js

## Build & Test Workflow

```bash
# Build everything
bazel build //...

# Test Python (Bazel)
bazel test //packages/...

# Test all languages (Python runner)
python3 tools/test_runners.py

# Build and test everything (CI/CD style)
./test_all.sh
```

## Test Details

### Python Tests
- Location: `packages/*/tests/test_*.py`
- Runner: pytest via Bazel rules
- Command: `bazel test //packages/...`

### Java Tests
```
Location: src/hildie/java/hildie-java-lib/src/test/java/
Classes:
  - HildieLibraryTest.testGreet()
  - HildieLibraryTest.testAdd()
```

### Go Tests
```
Location: src/hildie/go/lib/lib_test.go
Tests:
  - TestGreet
  - TestAdd
```

### Rust Tests
```
Location: src/hildie/rust/hildie-lib/src/lib.rs
Tests (inline):
  - test_greet()
  - test_add()
```

### Node.js Tests
```
Location: src/hildie/node/src/lib.test.ts
Tests:
  - greet()
  - add()
```

## Testing Tips

### Run tests in development
```bash
# All languages at once
./test_all.sh

# Specific language
cd src/hildie/rust && cargo test
cd src/hildie/go && go test ./...
cd src/hildie/node && npm test
```

### Watch for test output
```bash
python3 tools/test_runners.py 2>&1 | grep -E "PASSED|FAILED|Error"
```

### Debug a failing test
```bash
# Run specific language directly
cd src/hildie/java/hildie-java-lib
javac -d bin src/main/java/io/hildie/HildieLibrary.java src/test/java/io/hildie/HildieLibraryTest.java
java -ea -cp bin io.hildie.HildieLibraryTest
```

## Test Results Summary

```
✅ Python Tests:    6/6 PASSED
✅ Java Tests:      2/2 PASSED
✅ Go Tests:        2/2 PASSED
✅ Rust Tests:      2/2 PASSED
✅ Node.js Tests:   2/2 PASSED
─────────────────────────────
✅ TOTAL:          14+/14+ PASSED
```

## Adding New Tests

### Python
Add test file to `packages/*/tests/test_*.py`

### Java
Add test class to `src/hildie/java/hildie-java-lib/src/test/java/`

### Go
Add `*_test.go` file to test directory

### Rust
Add test functions with `#[cfg(test)]` attribute

### Node.js
Add `.test.ts` file and import in test suite

---

**All tests are automated and integrated into the development workflow.**
