// function to calculate the area of 3 polygons...
package main

import "fmt"

func main() {
	var option string
	var radius float32
	var length float32
	var breadth float32
	var side float32
	fmt.Println("\nAREA AND PERIMETER CALCULATION\n1.circle\n2.rectangle\n3.square")
	fmt.Println("choose your option")
	fmt.Scan(&option)
	if option == "1" {
		fmt.Println("Enter radius of the circle: ")
		fmt.Scan(&radius)
		area := 3.14 * radius * radius
		perimeter := 2 * 3.14 * radius
		fmt.Println("The area of the circle is: ", area)
		fmt.Println("The perimeter of the circle is: ", perimeter)
	} else if option == "2" {
		fmt.Println("Enter the length of the rectangle: ")
		fmt.Scan(&length)
		fmt.Println("Enter the breadth of the rectangle: ")
		fmt.Scan(&breadth)
		area := length * breadth
		perimeter := 2 * (length + breadth)
		fmt.Println("The area of the rectangle is: ", area)
		fmt.Println("The perimeter of the rectangle is: ", perimeter)
	} else if option == "3" {
		fmt.Println("Enter the length of square side: ")
		fmt.Scan(&side)
		area := side * side
		perimeter := 2 * side
		fmt.Println("The area of the square is: ", area)
		fmt.Println("The perimeter of the square is: ", perimeter)
	} else {
		fmt.Println("Thank you")
	}
}
