package main

import (
	"fmt"
	"time"
)

func main() {
	var userName string
	fmt.Printf("Enter your name:")
	fmt.Scan(&userName)
	fmt.Println("Hello, Welcome", userName, ".Date and time is ", time.Now())
}
