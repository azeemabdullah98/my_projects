package main

import (
	"fmt"
	"math/rand"
	"time"
)

func main() {
	var min int = 0
	var max int = 100
	rand.Seed(time.Now().UnixNano())
	fmt.Println(rand.Intn(max-min+1) + min)
}
