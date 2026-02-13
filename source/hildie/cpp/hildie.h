#ifndef HILDIE_H
#define HILDIE_H

#ifdef __cplusplus
extern "C" {
#endif

// Process data array
int* process_data(int* data, int size);

// Compute factorial
long factorial(int n);

// Free allocated memory
void free_memory(void* ptr);

#ifdef __cplusplus
}
#endif

#endif // HILDIE_H
