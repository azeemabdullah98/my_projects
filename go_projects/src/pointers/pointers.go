package main

import "fmt"

func main() {
	var x int = 3
	var y *int
	var z int
	y = &x
	z = *y
	fmt.Printf("value is %d\n", z)
}
