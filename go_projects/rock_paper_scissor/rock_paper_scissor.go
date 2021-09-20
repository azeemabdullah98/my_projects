package main

import "fmt"

func main() {
	var user1 string
	var user2 string
	var user1point int = 0
	var user2point int = 0
	fmt.Println("WELCOME TO ROCK, PAPER AND SCISSOR GAME!!!")
	fmt.Println("Best of three matches")
	for i := 0; i < 3; i++ {
		fmt.Println("user1\nEnter your choice:\n1.rock\n2.paper\n3.scissor")
		fmt.Scan(&user1)
		fmt.Println("user2\nenter your choice:\n1.rock\n2.paper\n3.scissor")
		fmt.Scan(&user2)
		if user1 == user2 {
			fmt.Println("Game Tie in ", i+1, "th attempt")
		} else if user1 == "2" && user2 == "1" || user1 == "1" && user2 == "3" || user1 == "3" && user2 == "2" {
			fmt.Println("user1 won the game in attempt ", i+1)
			user1point += 1
		} else {
			fmt.Println("user2 won the game in attempt ", i+1)
			user2point += 1
		}
	}
	fmt.Println("user1 score is ", user1point, " and user2 score is ", user2point)
	if user1point > user2point {
		fmt.Print("user1 won the game")
	} else if user2point > user1point {
		fmt.Println("user2 won the game")
	} else {
		fmt.Println("Game Tie")
	}

}
