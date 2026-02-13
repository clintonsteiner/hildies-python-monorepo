"""
Python bindings for Hildie C++ components

Uses ctypes to call compiled C++ shared library.
Requires: g++ -shared -fPIC -o libhildie_cpp.so cpp/hildie.cpp
"""

import ctypes
import os

# Try to load the C++ shared library
_lib_path: str | None = None

# Search for the library in multiple locations
_search_paths = [
    "libhildie_cpp.so",  # Linux
    "libhildie_cpp.dylib",  # macOS
    "libhildie_cpp.dll",  # Windows
    os.path.join(os.path.dirname(__file__), "lib", "libhildie_cpp.so"),
    os.path.join(os.path.dirname(__file__), "lib", "libhildie_cpp.dylib"),
    os.path.join(os.path.dirname(__file__), "lib", "libhildie_cpp.dll"),
]

for path in _search_paths:
    if os.path.exists(path):
        _lib_path = path
        break

if _lib_path:
    _hildie_cpp = ctypes.CDLL(_lib_path)
else:
    _hildie_cpp = None
    import warnings

    warnings.warn(
        "Hildie C++ bindings not found. Install with: "
        "cd source/hildie/cpp && g++ -shared -fPIC -o libhildie_cpp.so *.cpp",
        RuntimeWarning,
        stacklevel=2,
    )


def process_data(data: list[int]) -> list[int]:
    """Process data using C++ library.

    Args:
        data: List of integers to process

    Returns:
        Processed data
    """
    if _hildie_cpp is None:
        raise ImportError("C++ bindings not loaded. Please compile libhildie_cpp first.")

    # Define the C++ function signature
    # C++: int* process_data(int* data, int size)
    _hildie_cpp.process_data.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_int]
    _hildie_cpp.process_data.restype = ctypes.POINTER(ctypes.c_int)

    # Convert Python list to C array
    c_array = (ctypes.c_int * len(data))(*data)

    # Call C++ function
    result_ptr = _hildie_cpp.process_data(c_array, len(data))

    # Convert C array back to Python list
    result = list(result_ptr[: len(data)])

    # Free C++ allocated memory
    _hildie_cpp.free_memory(result_ptr)

    return result


def compute_factorial(n: int) -> int:
    """Compute factorial using C++ library.

    Args:
        n: Number to compute factorial for

    Returns:
        Factorial result
    """
    if _hildie_cpp is None:
        raise ImportError("C++ bindings not loaded. Please compile libhildie_cpp first.")

    # Define the C++ function signature
    # C++: long factorial(int n)
    _hildie_cpp.factorial.argtypes = [ctypes.c_int]
    _hildie_cpp.factorial.restype = ctypes.c_long

    return _hildie_cpp.factorial(n)
