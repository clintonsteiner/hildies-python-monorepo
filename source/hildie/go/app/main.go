package main

import (
	"fmt"
	"github.com/clintonsteiner/hildie-go/lib"
)

func main() {
	fmt.Println(lib.Greet("Hildie User"))
	fmt.Printf("2 + 3 = %d\n", lib.Add(2, 3))
}
