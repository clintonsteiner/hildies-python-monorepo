package main

import (
	"flag"
	"fmt"
	"github.com/clintonsteiner/hildie-go/lib"
)

func main() {
	if flag.NArg() == 0 {
		fmt.Println("Usage: hildie-cli <name>")
		return
	}

	name := flag.Arg(0)
	fmt.Println(lib.Greet(name))
}
