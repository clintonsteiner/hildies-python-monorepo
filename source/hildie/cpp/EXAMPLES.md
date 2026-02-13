# Hildie C++ Examples

This directory contains examples demonstrating the Hildie C++ library and its Python bindings.

## Files

- `hildie.h` - C/C++ header defining public interfaces
- `hildie.cpp` - C++ implementation
- `example.cpp` - Comprehensive example demonstrating all features

## Building the Example

### Compile Example Executable

```bash
# Using g++
g++ -std=c++17 -o hildie_example src/hildie/cpp/example.cpp src/hildie/cpp/hildie.cpp

# Using clang++
clang++ -std=c++17 -o hildie_example src/hildie/cpp/example.cpp src/hildie/cpp/hildie.cpp

# With optimization
g++ -std=c++17 -O2 -o hildie_example src/hildie/cpp/example.cpp src/hildie/cpp/hildie.cpp
```

### Run Example

```bash
./hildie_example
```

### Expected Output

```
=== Hildie C++ Bindings Example ===

Example 1: Process Data
------------------------
Input:   [1, 2, 3, 4, 5]
Output:  [2, 4, 6, 8, 10]
Behavior: Each element is multiplied by 2
Python usage:
  result = process_data([1, 2, 3, 4, 5])
  # result == [2, 4, 6, 8, 10]

Example 2: Process Data with Various Inputs
--------------------------------------------
Empty array: [] -> []
Single:  [7] -> [14]
Negatives: [-1, -2, -3]
Result:    [-2, -4, -6]
Python usage:
  result = process_data([-1, -2, -3])
  # result == [-2, -4, -6]

Example 3: Compute Factorial
-----------------------------
Factorial values:
  factorial(0) = 1
  factorial(1) = 1
  factorial(5) = 120
  factorial(6) = 720
  factorial(10) = 3628800

Python usage:
  result = compute_factorial(5)
  # result == 120

Example 4: Large Factorial
--------------------------
factorial(20) = 2432902008176640000

Python usage:
  result = compute_factorial(20)
  # result == 2432902008176640000

Example 5: Complex Scenario
---------------------------
Processing array and computing factorial of result:
Input array:     [1, 2, 3, 4, 5]
Processed (×2):  [2, 4, 6, 8, 10]
Factorial of array size (5): 120

Python equivalent:
  data = [1, 2, 3, 4, 5]
  processed = process_data(data)  # [2, 4, 6, 8, 10]
  fact = compute_factorial(len(data))  # factorial(5) = 120

Example 6: Using Bindings from Python
--------------------------------------
Import and use the bindings:

  from hildie_bindings import process_data, compute_factorial

  # Process an array
  data = [10, 20, 30]
  result = process_data(data)
  print(result)  # Output: [20, 40, 60]

  # Compute factorial
  fact = compute_factorial(5)
  print(fact)  # Output: 120

=== Example Complete ===
```

## Building the Shared Library for Python Bindings

```bash
# Compile to shared library (.so for Linux/macOS, .dll for Windows)
g++ -shared -fPIC -std=c++17 -o libhildie_cpp.so src/hildie/cpp/hildie.cpp

# macOS may use .dylib instead
g++ -shared -fPIC -std=c++17 -o libhildie_cpp.dylib src/hildie/cpp/hildie.cpp

# Windows may use .dll
g++ -shared -fPIC -std=c++17 -o libhildie_cpp.dll src/hildie/cpp/hildie.cpp
```

### Copy to Python Bindings Location

```bash
# Create lib directory if needed
mkdir -p src/hildie/bindings/python/hildie_bindings/lib

# Copy compiled library
cp libhildie_cpp.so src/hildie/bindings/python/hildie_bindings/lib/

# Or use build script
python3 tools/build_bindings.py --cpp
```

## C++ API Reference

### `int* process_data(int* data, int size)`

Processes an integer array by multiplying each element by 2.

**Parameters**:
- `data`: Pointer to input array
- `size`: Number of elements

**Returns**: Pointer to newly allocated output array (caller must free)

**Example**:
```cpp
int input[] = {1, 2, 3};
int* result = process_data(input, 3);
// result now points to [2, 4, 6]
free_memory(result);  // Don't forget to free!
```

### `long factorial(int n)`

Computes the factorial of n.

**Parameters**:
- `n`: Non-negative integer

**Returns**: Factorial value as long

**Example**:
```cpp
long fact = factorial(5);  // Returns 120
```

### `void free_memory(void* ptr)`

Frees memory allocated by C++ functions.

**Parameters**:
- `ptr`: Pointer to memory allocated by process_data

**Example**:
```cpp
int* result = process_data(data, size);
// ... use result ...
free_memory(result);  // Free when done
```

## Python Integration

### Using with Python Bindings

```python
from hildie_bindings import process_data, compute_factorial

# Process data
data = [1, 2, 3, 4, 5]
result = process_data(data)
print(result)  # [2, 4, 6, 8, 10]

# Compute factorial
fact = compute_factorial(5)
print(fact)  # 120
```

### What Happens Under the Hood

1. **C++ Code**: `process_data` and `factorial` are compiled to machine code in `libhildie_cpp.so`
2. **ctypes Wrapper**: `cpp_bindings.py` uses ctypes to call the compiled functions
3. **Type Conversion**: Python lists are converted to C arrays and back
4. **Memory Management**: Python handles memory cleanup

## Performance Characteristics

### process_data()

- **Time Complexity**: O(n) - iterates through array once
- **Space Complexity**: O(n) - allocates new array for results
- **Memory**: Each element uses 4 bytes (int)

For array size 1,000:
```cpp
int arr[1000];
int* result = process_data(arr, 1000);  // ~20 microseconds
```

### factorial()

- **Time Complexity**: O(n)
- **Space Complexity**: O(1) - constant memory
- **Accuracy**: Safe up to factorial(20), beyond that results may overflow

## Compilation Flags Explained

- `-shared`: Builds a shared library instead of executable
- `-fPIC`: Position Independent Code (required for shared libraries)
- `-std=c++17`: Uses C++17 standard
- `-O2`: Optimization level (faster code, longer compile time)

## Memory Management

### Important Notes

```cpp
// MUST call free_memory on pointers from process_data
int* result = process_data(data, size);
// ... use result ...
free_memory(result);  // Required!

// Do NOT use delete directly
// delete[] result;  // Wrong! Use free_memory instead
```

### Why free_memory?

The `free_memory` function uses the C++ delete operator. If you mix memory allocators (malloc vs new), you'll get undefined behavior. Always use the provided function.

## Troubleshooting

### "libhildie_cpp.so: cannot open shared object file"

**Cause**: Library not found in expected locations

**Solution**:
```bash
python3 tools/build_bindings.py --cpp
```

### "undefined reference to `process_data`"

**Cause**: Didn't link against compiled library

**Solution**: When compiling C++ code that uses these functions:
```bash
g++ -std=c++17 your_code.cpp hildie.cpp -o your_program
```

### "Segmentation fault"

**Cause**: Usually from not calling `free_memory()` or using invalid pointers

**Solution**:
```cpp
// Always free memory from process_data
int* result = process_data(data, size);
free_memory(result);

// Don't use result after freeing
free_memory(result);
// result = nullptr;  // Good practice
```

### Compiler not found

**Solution**: Install build tools:
```bash
# Ubuntu/Debian
sudo apt-get install build-essential

# macOS
xcode-select --install

# Windows
# Install MinGW or Visual Studio
```

## Example Use Cases

### 1. Batch Processing

```cpp
#include "hildie.h"

int main() {
    int batches[100];
    for (int i = 0; i < 100; i++) {
        int batch[] = {i, i+1, i+2};
        int* result = process_data(batch, 3);
        // Use result...
        free_memory(result);
    }
    return 0;
}
```

### 2. Computing Combinatorics

```cpp
#include "hildie.h"

long combination(int n, int k) {
    long n_fact = factorial(n);
    long k_fact = factorial(k);
    long nk_fact = factorial(n - k);
    return n_fact / (k_fact * nk_fact);
}
```

### 3. Data Validation

```cpp
#include "hildie.h"

bool validate_factorial(int n, long expected) {
    return factorial(n) == expected;
}
```

## Extending with More Functions

To add new functions:

1. **Update Header** (`hildie.h`):
```cpp
int multiply(int a, int b);
```

2. **Implement Function** (`hildie.cpp`):
```cpp
int multiply(int a, int b) {
    return a * b;
}
```

3. **Add ctypes Wrapper** (`cpp_bindings.py`):
```python
def multiply_cpp(a: int, b: int) -> int:
    if _hildie_cpp is None:
        raise ImportError("C++ bindings not loaded")
    _hildie_cpp.multiply.argtypes = [ctypes.c_int, ctypes.c_int]
    _hildie_cpp.multiply.restype = ctypes.c_int
    return _hildie_cpp.multiply(a, b)
```

4. **Export from Python** (`__init__.py`):
```python
from .cpp_bindings import multiply_cpp
```

5. **Add Tests**:
```python
def test_multiply_cpp_basic(self):
    assert multiply_cpp(3, 4) == 12
```

## Testing Example Code

```bash
# Compile example
g++ -std=c++17 -o hildie_example src/hildie/cpp/example.cpp src/hildie/cpp/hildie.cpp

# Run example
./hildie_example

# Verify output
./hildie_example | grep "Example 1" -A 5
```

## See Also

- [Python Bindings README](../bindings/python/README.md)
- [Python Bindings Testing](../bindings/python/TESTING.md)
- [Hildie Namespaces](../../HILDIE_NAMESPACES.md)
