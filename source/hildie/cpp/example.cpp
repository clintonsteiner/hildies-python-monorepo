/**
 * Hildie C++ Example - Demonstrates Python Bindings
 *
 * This example shows:
 * - How to use Hildie C++ functions directly in C++
 * - How these functions are exposed to Python via ctypes
 * - Expected behavior for Python developers
 */

#include "hildie.h"
#include <iostream>
#include <vector>
#include <cstring>

// Helper function to print array
void print_array(int* data, int size, const char* label) {
    std::cout << label << " [";
    for (int i = 0; i < size; i++) {
        std::cout << data[i];
        if (i < size - 1) std::cout << ", ";
    }
    std::cout << "]\n";
}

int main() {
    std::cout << "=== Hildie C++ Bindings Example ===\n\n";

    // Example 1: Process data (multiply by 2)
    std::cout << "Example 1: Process Data\n";
    std::cout << "------------------------\n";

    int input1[] = {1, 2, 3, 4, 5};
    int size1 = 5;

    print_array(input1, size1, "Input:  ");

    int* output1 = process_data(input1, size1);
    print_array(output1, size1, "Output: ");

    std::cout << "Behavior: Each element is multiplied by 2\n";
    std::cout << "Python usage:\n";
    std::cout << "  result = process_data([1, 2, 3, 4, 5])\n";
    std::cout << "  # result == [2, 4, 6, 8, 10]\n\n";

    free_memory(output1);

    // Example 2: Process data with different inputs
    std::cout << "Example 2: Process Data with Various Inputs\n";
    std::cout << "--------------------------------------------\n";

    // Empty array
    int* empty_result = process_data(nullptr, 0);
    std::cout << "Empty array: [] -> []\n";

    // Single element
    int single[] = {7};
    int* single_result = process_data(single, 1);
    print_array(single_result, 1, "Single:  [7] -> ");
    free_memory(single_result);

    // Negative numbers
    int negatives[] = {-1, -2, -3};
    int* neg_result = process_data(negatives, 3);
    print_array(negatives, 3, "Negatives: ");
    print_array(neg_result, 3, "Result:    ");
    std::cout << "Python usage:\n";
    std::cout << "  result = process_data([-1, -2, -3])\n";
    std::cout << "  # result == [-2, -4, -6]\n\n";
    free_memory(neg_result);

    // Example 3: Compute factorial
    std::cout << "Example 3: Compute Factorial\n";
    std::cout << "-----------------------------\n";

    int test_values[] = {0, 1, 5, 6, 10};
    std::cout << "Factorial values:\n";
    for (int val : test_values) {
        long fact = factorial(val);
        std::cout << "  factorial(" << val << ") = " << fact << "\n";
    }

    std::cout << "\nPython usage:\n";
    std::cout << "  result = compute_factorial(5)\n";
    std::cout << "  # result == 120\n\n";

    // Example 4: Demonstrate large factorial
    std::cout << "Example 4: Large Factorial\n";
    std::cout << "--------------------------\n";

    int large_n = 20;
    long large_fact = factorial(large_n);
    std::cout << "factorial(" << large_n << ") = " << large_fact << "\n";
    std::cout << "Python usage:\n";
    std::cout << "  result = compute_factorial(20)\n";
    std::cout << "  # result == " << large_fact << "\n\n";

    // Example 5: Complex scenario
    std::cout << "Example 5: Complex Scenario\n";
    std::cout << "---------------------------\n";
    std::cout << "Processing array and computing factorial of result:\n";

    int complex_input[] = {1, 2, 3, 4, 5};
    int complex_size = 5;

    print_array(complex_input, complex_size, "Input array:    ");

    int* processed = process_data(complex_input, complex_size);
    print_array(processed, complex_size, "Processed (×2): ");

    // Use size of array as factorial input
    long fact_of_size = factorial(complex_size);
    std::cout << "Factorial of array size (" << complex_size << "): " << fact_of_size << "\n";

    std::cout << "\nPython equivalent:\n";
    std::cout << "  data = [1, 2, 3, 4, 5]\n";
    std::cout << "  processed = process_data(data)  # [2, 4, 6, 8, 10]\n";
    std::cout << "  fact = compute_factorial(len(data))  # factorial(5) = 120\n\n";

    free_memory(processed);

    // Example 6: Error handling in Python
    std::cout << "Example 6: Using Bindings from Python\n";
    std::cout << "--------------------------------------\n";
    std::cout << "Import and use the bindings:\n\n";
    std::cout << "  from hildie_bindings import process_data, compute_factorial\n\n";
    std::cout << "  # Process an array\n";
    std::cout << "  data = [10, 20, 30]\n";
    std::cout << "  result = process_data(data)\n";
    std::cout << "  print(result)  # Output: [20, 40, 60]\n\n";
    std::cout << "  # Compute factorial\n";
    std::cout << "  fact = compute_factorial(5)\n";
    std::cout << "  print(fact)  # Output: 120\n\n";

    std::cout << "=== Example Complete ===\n";
    return 0;
}
