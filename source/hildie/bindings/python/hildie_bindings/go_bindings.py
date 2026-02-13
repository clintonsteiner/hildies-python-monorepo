"""
Python bindings for Hildie Go library

Uses ctypes to call compiled Go shared library.
Requires: go build -o libhildie_go.so -buildmode=c-shared ./source/hildie/go
"""

import ctypes
import os

# Try to load the Go shared library
_lib_path: str | None = None

# Search for the library in multiple locations
_search_paths = [
    "libhildie_go.so",  # Current directory
    "libhildie_go.dylib",  # macOS
    "libhildie_go.dll",  # Windows
    os.path.join(os.path.dirname(__file__), "lib", "libhildie_go.so"),
    os.path.join(os.path.dirname(__file__), "lib", "libhildie_go.dylib"),
    os.path.join(os.path.dirname(__file__), "lib", "libhildie_go.dll"),
]

for path in _search_paths:
    if os.path.exists(path):
        _lib_path = path
        break

if _lib_path:
    _hildie_go = ctypes.CDLL(_lib_path)
else:
    _hildie_go = None
    import warnings

    warnings.warn(
        "Hildie Go bindings not found. Install with: "
        "cd source/hildie/go && go build -o libhildie_go.so -buildmode=c-shared ./...",
        RuntimeWarning,
        stacklevel=2,
    )


def greet_go(name: str) -> str:
    """Greet a person using Go library.

    Args:
        name: Name to greet

    Returns:
        Greeting string from Go
    """
    if _hildie_go is None:
        raise ImportError("Go bindings not loaded. Please compile libhildie_go first.")

    # Define the Go function signature
    # Go: func Greet(name string) string
    _hildie_go.Greet.argtypes = [ctypes.c_char_p]
    _hildie_go.Greet.restype = ctypes.c_char_p

    result = _hildie_go.Greet(name.encode("utf-8"))
    return result.decode("utf-8")


def add_go(a: int, b: int) -> int:
    """Add two numbers using Go library.

    Args:
        a: First number
        b: Second number

    Returns:
        Sum from Go
    """
    if _hildie_go is None:
        raise ImportError("Go bindings not loaded. Please compile libhildie_go first.")

    # Define the Go function signature
    # Go: func Add(a, b int) int
    _hildie_go.Add.argtypes = [ctypes.c_int, ctypes.c_int]
    _hildie_go.Add.restype = ctypes.c_int

    return _hildie_go.Add(a, b)
