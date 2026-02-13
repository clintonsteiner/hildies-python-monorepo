package lib

import (
	"testing"
)

func TestGreet(t *testing.T) {
	expected := "Hello from Hildie Go Library, World!"
	result := Greet("World")
	if result != expected {
		t.Errorf("Expected %s, got %s", expected, result)
	}
}

func TestAdd(t *testing.T) {
	result := Add(2, 3)
	if result != 5 {
		t.Errorf("Expected 5, got %d", result)
	}
}
