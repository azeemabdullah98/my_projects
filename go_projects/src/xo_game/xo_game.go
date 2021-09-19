package main

import (
	"fmt"
	"strings"
)

func board() {
	// Create a tic-tac-toe board.
	board := [][]string{
		{"_", "_", "_"},
		{"_", "_", "_"},
		{"_", "_", "_"},
	}
	for i := 0; i < len(board); i++ {
		fmt.Printf("%s\n", strings.Join(board[i], " "))
	}
}

func main() {
	var user string
	var userChoice int
	var comp string
	var compChoice int
	fmt.Println("Welcome to tic-tac-toe game!!!")
	fmt.Println("Enter user choice: 'X' or 'O'")
	fmt.Scan(&user)
	if user == "X" {
		comp = "O"
	} else if user == "O" {
		comp = "X"
	}
	board()
	fmt.Println("Enter the user choice of position: ")
	fmt.Scan(&userChoice)
	
}
