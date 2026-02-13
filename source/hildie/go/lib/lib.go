package lib

import "fmt"

// Greet returns a greeting message
func Greet(name string) string {
	return fmt.Sprintf("Hello from Hildie Go Library, %s!", name)
}

// Add returns the sum of two integers
func Add(a, b int) int {
	return a + b
}
