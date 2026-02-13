"""
Hildie Python Bindings

Provides Python interfaces to:
- Rust library (via PyO3)
- Go library (via ctypes)
- C++ components (via ctypes)
"""

# Import Rust bindings
try:
    from hildie_bindings import (
        greet_all,
    )
    from hildie_bindings import (
        py_add as add_rust,
    )
    from hildie_bindings import (
        py_greet as greet_rust,
    )
except ImportError:
    # Fallback if bindings not compiled
    greet_rust = None
    add_rust = None
    greet_all = None

# Import Go bindings
# Import C++ bindings
from .cpp_bindings import (
    compute_factorial,
    process_data,
)
from .go_bindings import (
    add_go,
    greet_go,
)

__all__ = [
    # Rust
    "greet_rust",
    "add_rust",
    "greet_all",
    # Go
    "greet_go",
    "add_go",
    # C++
    "process_data",
    "compute_factorial",
]
