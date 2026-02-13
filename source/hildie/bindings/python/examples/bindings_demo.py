#!/usr/bin/env python3
"""
Hildie Python Bindings Demo

Demonstrates usage of:
- Rust bindings (PyO3)
- Go bindings (ctypes)
- C++ bindings (ctypes)
"""

import sys
from pathlib import Path

# Add parent directory to path to import bindings
sys.path.insert(0, str(Path(__file__).parent.parent))

from hildie_bindings import (
    add_go,
    add_rust,
    compute_factorial,
    greet_all,
    greet_go,
    greet_rust,
    process_data,
)


def demo_rust_bindings():
    """Demonstrate Rust bindings."""
    print("\n" + "=" * 60)
    print("RUST BINDINGS (via PyO3)")
    print("=" * 60)

    # Greet function
    print("\n1. Greet Function")
    print("-" * 60)
    for name in ["Alice", "Bob", "Charlie"]:
        result = greet_rust(name)
        print(f"greet_rust('{name}') -> {result}")

    # Add function
    print("\n2. Add Function")
    print("-" * 60)
    test_cases = [(2, 3), (10, 20), (-5, 10), (0, 42)]
    for a, b in test_cases:
        result = add_rust(a, b)
        print(f"add_rust({a}, {b}) -> {result}")

    # Greet all function
    print("\n3. Greet All Function")
    print("-" * 60)
    result = greet_all("Alice", "Bob", "Charlie", "Diana")
    print(f"greet_all('Alice', 'Bob', 'Charlie', 'Diana') -> {result}")


def demo_go_bindings():
    """Demonstrate Go bindings."""
    print("\n" + "=" * 60)
    print("GO BINDINGS (via ctypes)")
    print("=" * 60)

    try:
        # Greet function
        print("\n1. Greet Function")
        print("-" * 60)
        for name in ["Alice", "Bob", "Charlie"]:
            result = greet_go(name)
            print(f"greet_go('{name}') -> {result}")

        # Add function
        print("\n2. Add Function")
        print("-" * 60)
        test_cases = [(2, 3), (10, 20), (-5, 10), (0, 42)]
        for a, b in test_cases:
            result = add_go(a, b)
            print(f"add_go({a}, {b}) -> {result}")

    except ImportError as e:
        print(f"⚠️  Go bindings not available: {e}")
        print(
            "   Build with: cd source/hildie/go && go build -buildmode=c-shared -o libhildie_go.so ./..."
        )


def demo_cpp_bindings():
    """Demonstrate C++ bindings."""
    print("\n" + "=" * 60)
    print("C++ BINDINGS (via ctypes)")
    print("=" * 60)

    try:
        # Process data function
        print("\n1. Process Data Function (multiply by 2)")
        print("-" * 60)
        test_arrays = [
            [1, 2, 3, 4, 5],
            [10, 20, 30],
            [-1, -2, -3],
            [0, 5, 10],
        ]
        for arr in test_arrays:
            result = process_data(arr)
            print(f"process_data({arr}) -> {result}")

        # Compute factorial function
        print("\n2. Compute Factorial Function")
        print("-" * 60)
        test_values = [0, 1, 5, 6, 10]
        for n in test_values:
            result = compute_factorial(n)
            print(f"compute_factorial({n}) -> {result}")

        # Complex example
        print("\n3. Complex Example")
        print("-" * 60)
        data = [1, 2, 3, 4, 5]
        processed = process_data(data)
        fact_of_size = compute_factorial(len(data))
        print(f"Original data:        {data}")
        print(f"Processed (×2):       {processed}")
        print(f"Factorial of size:    {fact_of_size}")
        print(f"Sum of processed:     {sum(processed)}")
        print(
            f"Product of processed: {1 if not processed else eval('*'.join(map(str, processed)))}"
        )

    except ImportError as e:
        print(f"⚠️  C++ bindings not available: {e}")
        print("   Build with: g++ -shared -fPIC -o libhildie_cpp.so source/hildie/cpp/hildie.cpp")


def demo_cross_language_consistency():
    """Demonstrate consistency across languages."""
    print("\n" + "=" * 60)
    print("CROSS-LANGUAGE CONSISTENCY CHECK")
    print("=" * 60)

    try:
        print("\n1. Addition Consistency (Rust vs Go)")
        print("-" * 60)
        test_cases = [(2, 3), (10, 20), (-5, 10), (0, 42)]
        for a, b in test_cases:
            rust_result = add_rust(a, b)
            go_result = add_go(a, b)
            match = "✓" if rust_result == go_result else "✗"
            print(f"{match} add({a}, {b}): Rust={rust_result}, Go={go_result}")

        print("\n2. Greeting Consistency (Rust vs Go)")
        print("-" * 60)
        names = ["Alice", "Bob", "Charlie"]
        for name in names:
            rust_result = greet_rust(name)
            go_result = greet_go(name)
            rust_has_name = name in rust_result
            go_has_name = name in go_result
            match = "✓" if (rust_has_name and go_has_name) else "✗"
            print(
                f"{match} greet('{name}'): Rust contains name={rust_has_name}, Go contains name={go_has_name}"
            )

    except ImportError as e:
        print(f"⚠️  Cannot compare: {e}")


def demo_error_handling():
    """Demonstrate error handling."""
    print("\n" + "=" * 60)
    print("ERROR HANDLING")
    print("=" * 60)

    # Python type conversion
    print("\n1. Type Handling")
    print("-" * 60)
    print("Processing empty list:", process_data([]))
    print("Processing single element:", process_data([5]))
    print("Processing large array:", len(process_data(list(range(1, 101)))), "elements")

    # Factorial edge cases
    print("\n2. Factorial Edge Cases")
    print("-" * 60)
    print("compute_factorial(0) =", compute_factorial(0))
    print("compute_factorial(1) =", compute_factorial(1))


def main():
    """Run all demonstrations."""
    print("\n" + "#" * 60)
    print("# Hildie Python Bindings - Complete Demonstration")
    print("#" * 60)

    demo_rust_bindings()
    demo_go_bindings()
    demo_cpp_bindings()
    demo_cross_language_consistency()
    demo_error_handling()

    print("\n" + "#" * 60)
    print("# Demonstration Complete")
    print("#" * 60 + "\n")


if __name__ == "__main__":
    main()
