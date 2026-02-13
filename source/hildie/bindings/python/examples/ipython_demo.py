#!/usr/bin/env python3
"""
IPython-compatible demo of Hildie bindings.

This script works both in IPython and regular Python.
Each function is designed to be copy-pasted into an IPython cell.
"""

import sys
from pathlib import Path

# Add parent directory to path
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


def setup_ipython():
    """Configure IPython display if available."""
    try:
        from IPython.display import HTML, display

        return True, display, HTML
    except ImportError:
        return False, print, lambda x: x


def demo_1_rust_greet():
    """Demo 1: Rust Greeting"""
    is_ipython, display_fn, html = setup_ipython()

    if is_ipython:
        display_fn(html("<h3>Demo 1: Rust Greetings</h3>"))
    else:
        print("\n=== Demo 1: Rust Greetings ===\n")

    names = ["Alice", "Bob", "Charlie"]
    for name in names:
        result = greet_rust(name)
        print(f"greet_rust('{name}') → {result}")

    return names


def demo_2_rust_math():
    """Demo 2: Rust Addition"""
    is_ipython, display_fn, html = setup_ipython()

    if is_ipython:
        display_fn(html("<h3>Demo 2: Rust Math</h3>"))
    else:
        print("\n=== Demo 2: Rust Math ===\n")

    test_cases = [(2, 3), (10, 20), (-5, 15)]
    results = []

    for a, b in test_cases:
        result = add_rust(a, b)
        results.append(result)
        print(f"add_rust({a}, {b}) = {result}")

    return results


def demo_3_rust_greet_all():
    """Demo 3: Rust Greet All"""
    is_ipython, display_fn, html = setup_ipython()

    if is_ipython:
        display_fn(html("<h3>Demo 3: Rust Greet All</h3>"))
    else:
        print("\n=== Demo 3: Rust Greet All ===\n")

    result = greet_all("Alice", "Bob", "Charlie", "Diana")
    print(f"greet_all('Alice', 'Bob', 'Charlie', 'Diana'):\n{result}")

    return result


def demo_4_go_bindings():
    """Demo 4: Go Bindings"""
    is_ipython, display_fn, html = setup_ipython()

    if is_ipython:
        display_fn(html("<h3>Demo 4: Go Bindings</h3>"))
    else:
        print("\n=== Demo 4: Go Bindings ===\n")

    try:
        print("Go Greeting:")
        go_greet = greet_go("Go")
        print(f"  greet_go('Go') → {go_greet}")

        print("\nGo Addition:")
        go_add = add_go(5, 7)
        print(f"  add_go(5, 7) → {go_add}")

        return go_greet, go_add
    except ImportError as e:
        print(f"⚠️  Go bindings not available: {e}")
        return None, None


def demo_5_cpp_process_data():
    """Demo 5: C++ Data Processing"""
    is_ipython, display_fn, html = setup_ipython()

    if is_ipython:
        display_fn(html("<h3>Demo 5: C++ Data Processing</h3>"))
    else:
        print("\n=== Demo 5: C++ Data Processing ===\n")

    try:
        test_arrays = [
            [1, 2, 3, 4, 5],
            [10, 20, 30],
            [-1, -2, -3],
        ]

        results = []
        for arr in test_arrays:
            processed = process_data(arr)
            results.append(processed)
            print(f"process_data({arr})")
            print(f"  → {processed}")

        return results
    except ImportError as e:
        print(f"⚠️  C++ bindings not available: {e}")
        return None


def demo_6_cpp_factorial():
    """Demo 6: C++ Factorial"""
    is_ipython, display_fn, html = setup_ipython()

    if is_ipython:
        display_fn(html("<h3>Demo 6: C++ Factorial</h3>"))
    else:
        print("\n=== Demo 6: C++ Factorial ===\n")

    try:
        values = [0, 1, 5, 6, 10]
        results = {}

        for n in values:
            result = compute_factorial(n)
            results[n] = result
            print(f"compute_factorial({n:2d}) = {result}")

        return results
    except ImportError as e:
        print(f"⚠️  C++ bindings not available: {e}")
        return None


def demo_7_cross_language():
    """Demo 7: Cross-Language Consistency"""
    is_ipython, display_fn, html = setup_ipython()

    if is_ipython:
        display_fn(html("<h3>Demo 7: Cross-Language Consistency</h3>"))
    else:
        print("\n=== Demo 7: Cross-Language Consistency ===\n")

    try:
        print("Testing add() consistency between Rust and Go:")
        test_cases = [(5, 10), (100, 200), (-10, 20)]

        for a, b in test_cases:
            rust_result = add_rust(a, b)
            go_result = add_go(a, b)
            match = "✓" if rust_result == go_result else "✗"
            print(f"{match} add({a:4d}, {b:4d}): Rust={rust_result}, Go={go_result}")

        return True
    except Exception as e:
        print(f"⚠️  Error: {e}")
        return False


def run_all_demos():
    """Run all demos sequentially."""
    is_ipython, display_fn, html = setup_ipython()

    if is_ipython:
        display_fn(
            html("""
        <h2>Hildie Bindings - IPython Demo</h2>
        <p>Complete demonstration of Python bindings for Rust, Go, and C++</p>
        """)
        )
    else:
        print("\n" + "=" * 70)
        print("HILDIE BINDINGS - IPython Compatible Demo")
        print("=" * 70)

    results = {}

    try:
        results["demo_1"] = demo_1_rust_greet()
        results["demo_2"] = demo_2_rust_math()
        results["demo_3"] = demo_3_rust_greet_all()
        results["demo_4"] = demo_4_go_bindings()
        results["demo_5"] = demo_5_cpp_process_data()
        results["demo_6"] = demo_6_cpp_factorial()
        results["demo_7"] = demo_7_cross_language()

        if is_ipython:
            display_fn(html("<h3>Demo Complete!</h3>"))
        else:
            print("\n" + "=" * 70)
            print("Demo Complete!")
            print("=" * 70 + "\n")

        return results

    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
        import traceback

        traceback.print_exc()
        return None


if __name__ == "__main__":
    run_all_demos()
