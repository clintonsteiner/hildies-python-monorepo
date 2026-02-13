"""
Comprehensive tests for Hildie Python bindings.

Tests all language bindings:
- Rust (via PyO3)
- Go (via ctypes)
- C++ (via ctypes)
"""

import pytest
from hildie_bindings import (
    add_go,
    add_rust,
    compute_factorial,
    greet_all,
    greet_go,
    greet_rust,
    process_data,
)


class TestRustBindings:
    """Tests for Rust bindings via PyO3."""

    def test_greet_rust_basic(self):
        """Test basic greeting from Rust."""
        result = greet_rust("Alice")
        assert isinstance(result, str)
        assert "Alice" in result
        assert "Hello" in result or "hello" in result

    def test_greet_rust_empty_name(self):
        """Test greeting with empty name."""
        result = greet_rust("")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_greet_rust_special_chars(self):
        """Test greeting with special characters."""
        result = greet_rust("Alice & Bob")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_add_rust_basic(self):
        """Test basic addition in Rust."""
        result = add_rust(2, 3)
        assert result == 5
        assert isinstance(result, int)

    def test_add_rust_zero(self):
        """Test addition with zero."""
        assert add_rust(0, 5) == 5
        assert add_rust(5, 0) == 5
        assert add_rust(0, 0) == 0

    def test_add_rust_negative(self):
        """Test addition with negative numbers."""
        assert add_rust(-2, 3) == 1
        assert add_rust(-5, -3) == -8
        assert add_rust(10, -4) == 6

    def test_add_rust_large_numbers(self):
        """Test addition with large numbers."""
        result = add_rust(1000000, 2000000)
        assert result == 3000000

    def test_greet_all_basic(self):
        """Test greeting multiple names."""
        result = greet_all("Alice", "Bob", "Charlie")
        assert isinstance(result, str)
        assert len(result) > 0
        # Should mention multiple people
        assert result.count(",") >= 1 or len(result) > 20

    def test_greet_all_single_name(self):
        """Test greet_all with single name."""
        result = greet_all("Alice")
        assert isinstance(result, str)
        assert "Alice" in result

    def test_greet_all_empty(self):
        """Test greet_all with no names."""
        result = greet_all()
        assert isinstance(result, str)


class TestGoBindings:
    """Tests for Go bindings via ctypes."""

    @pytest.mark.skipif(not greet_go, reason="Go bindings not loaded")
    def test_greet_go_basic(self):
        """Test basic greeting from Go."""
        result = greet_go("Alice")
        assert isinstance(result, str)
        assert "Alice" in result
        assert "Hello" in result or "hello" in result

    @pytest.mark.skipif(not greet_go, reason="Go bindings not loaded")
    def test_greet_go_empty_name(self):
        """Test greeting with empty name."""
        result = greet_go("")
        assert isinstance(result, str)
        assert len(result) > 0

    @pytest.mark.skipif(not greet_go, reason="Go bindings not loaded")
    def test_greet_go_special_chars(self):
        """Test greeting with special characters."""
        result = greet_go("Bob & Alice")
        assert isinstance(result, str)
        assert len(result) > 0

    @pytest.mark.skipif(not add_go, reason="Go bindings not loaded")
    def test_add_go_basic(self):
        """Test basic addition in Go."""
        result = add_go(2, 3)
        assert result == 5
        assert isinstance(result, int)

    @pytest.mark.skipif(not add_go, reason="Go bindings not loaded")
    def test_add_go_zero(self):
        """Test addition with zero."""
        assert add_go(0, 5) == 5
        assert add_go(5, 0) == 5
        assert add_go(0, 0) == 0

    @pytest.mark.skipif(not add_go, reason="Go bindings not loaded")
    def test_add_go_negative(self):
        """Test addition with negative numbers."""
        assert add_go(-2, 3) == 1
        assert add_go(-5, -3) == -8
        assert add_go(10, -4) == 6

    @pytest.mark.skipif(not add_go, reason="Go bindings not loaded")
    def test_add_go_large_numbers(self):
        """Test addition with large numbers."""
        result = add_go(1000000, 2000000)
        assert result == 3000000


class TestCppBindings:
    """Tests for C++ bindings via ctypes."""

    @pytest.mark.skipif(not process_data, reason="C++ bindings not loaded")
    def test_process_data_basic(self):
        """Test basic data processing."""
        result = process_data([1, 2, 3, 4, 5])
        assert result == [2, 4, 6, 8, 10]

    @pytest.mark.skipif(not process_data, reason="C++ bindings not loaded")
    def test_process_data_empty(self):
        """Test data processing with empty list."""
        result = process_data([])
        assert result == []

    @pytest.mark.skipif(not process_data, reason="C++ bindings not loaded")
    def test_process_data_single(self):
        """Test data processing with single element."""
        result = process_data([5])
        assert result == [10]

    @pytest.mark.skipif(not process_data, reason="C++ bindings not loaded")
    def test_process_data_negative(self):
        """Test data processing with negative numbers."""
        result = process_data([-1, -2, -3])
        assert result == [-2, -4, -6]

    @pytest.mark.skipif(not process_data, reason="C++ bindings not loaded")
    def test_process_data_mixed(self):
        """Test data processing with mixed positive and negative."""
        result = process_data([-1, 0, 1, 2, -3])
        assert result == [-2, 0, 2, 4, -6]

    @pytest.mark.skipif(not process_data, reason="C++ bindings not loaded")
    def test_process_data_large(self):
        """Test data processing with large array."""
        data = list(range(1, 101))  # 1 to 100
        result = process_data(data)
        assert len(result) == 100
        assert result[0] == 2  # 1 * 2
        assert result[99] == 200  # 100 * 2

    @pytest.mark.skipif(not compute_factorial, reason="C++ bindings not loaded")
    def test_compute_factorial_basic(self):
        """Test basic factorial computation."""
        assert compute_factorial(5) == 120
        assert compute_factorial(4) == 24
        assert compute_factorial(3) == 6

    @pytest.mark.skipif(not compute_factorial, reason="C++ bindings not loaded")
    def test_compute_factorial_base_cases(self):
        """Test factorial base cases."""
        assert compute_factorial(0) == 1
        assert compute_factorial(1) == 1
        assert compute_factorial(2) == 2

    @pytest.mark.skipif(not compute_factorial, reason="C++ bindings not loaded")
    def test_compute_factorial_larger(self):
        """Test factorial with larger numbers."""
        assert compute_factorial(10) == 3628800
        assert compute_factorial(6) == 720

    @pytest.mark.skipif(not compute_factorial, reason="C++ bindings not loaded")
    def test_compute_factorial_sequence(self):
        """Test factorial sequence."""
        expected = [1, 1, 2, 6, 24, 120]
        for n, expected_fact in enumerate(expected):
            assert compute_factorial(n) == expected_fact


class TestCrossLanguageConsistency:
    """Tests to ensure consistency across language bindings."""

    def test_add_consistency_rust_go(self):
        """Verify Rust and Go add functions return same results."""
        test_cases = [
            (2, 3),
            (0, 0),
            (-5, 10),
            (100, 200),
        ]
        for a, b in test_cases:
            rust_result = add_rust(a, b)
            go_result = add_go(a, b)
            assert rust_result == go_result, f"Mismatch for add({a}, {b})"

    def test_greet_consistency_rust_go(self):
        """Verify Rust and Go greet functions both return non-empty strings."""
        names = ["Alice", "Bob", "Charlie"]
        for name in names:
            rust_result = greet_rust(name)
            go_result = greet_go(name)
            assert isinstance(rust_result, str)
            assert isinstance(go_result, str)
            assert len(rust_result) > 0
            assert len(go_result) > 0
            assert name in rust_result
            assert name in go_result


class TestErrorHandling:
    """Tests for error conditions and edge cases."""

    def test_process_data_returns_list(self):
        """Verify process_data always returns a list."""
        result = process_data([1])
        assert isinstance(result, list)

    def test_process_data_list_length_preserved(self):
        """Verify process_data preserves list length."""
        for length in [1, 5, 10, 100]:
            data = list(range(length))
            result = process_data(data)
            assert len(result) == length

    def test_greet_rust_returns_string(self):
        """Verify greet_rust always returns a string."""
        result = greet_rust("test")
        assert isinstance(result, str)

    def test_add_rust_returns_int(self):
        """Verify add_rust always returns an int."""
        result = add_rust(1, 2)
        assert isinstance(result, int)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
