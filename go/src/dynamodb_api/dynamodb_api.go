package main

import (
	"context"
	"fmt"
	"log"

	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/dynamodb"
)

func main() {
	cfg, err := config.LoadDefaultConfig(context.TODO(), config.WithRegion("us-east-2"))
	if err != nil {
		log.Fatal(err)
	}
	client := dynamodb.NewFromConfig(cfg)

	resp, err := client.Query(context.TODO(), &dynamodb.BatchRequest{
		TableName: aws.String("material_master"),
		Key:       aws.String("Std Text"),
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(resp)

}
