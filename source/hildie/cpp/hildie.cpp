#include "hildie.h"
#include <cstring>
#include <algorithm>

// Process data array - multiply each element by 2
int* process_data(int* data, int size) {
    int* result = new int[size];
    for (int i = 0; i < size; i++) {
        result[i] = data[i] * 2;
    }
    return result;
}

// Compute factorial
long factorial(int n) {
    if (n <= 1) return 1;
    long result = 1;
    for (int i = 2; i <= n; i++) {
        result *= i;
    }
    return result;
}

// Free allocated memory
void free_memory(void* ptr) {
    delete[] (int*)ptr;
}
