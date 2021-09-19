// number guess game...
package main

import (
	"fmt"
	"math/rand"
)

func main() {
	var min int = 0
	var max int = 100
	var option string
	var attempt int = 0
	fmt.Println("Think of a number between 0-100 and keep it with you, Let me find out!!!")
	for {
		num := rand.Intn(max-min+1) + min
		fmt.Println("Is'nt it?\n", num)
		fmt.Println("1.high\n2.low\n3.bingo")
		fmt.Scan(&option)
		if option == "1" || option == "high" {
			max = num - 1
			attempt += 1
			continue
		} else if option == "2" || option == "low" {
			min = num + 1
			attempt += 1
			continue
		} else if option == "3" || option == "bingo" {
			fmt.Println("you have guessed the number correct!!!")
			fmt.Println("The number in your mind is ", num, " and the computer took ", attempt, " attempts")
			break
		}
	}
}
