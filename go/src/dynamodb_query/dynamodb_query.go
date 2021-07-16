package main

import (
	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/dynamodb"
	"github.com/aws/aws-sdk-go/service/dynamodb/dynamodbattribute"
)

var dynamo *dynamodb.DynamoDB

// connectDynamo returns a dynamoDB client
func connectDynamo() (db *dynamodb.DynamoDB) {
	return dynamodb.New(session.Must(session.NewSession(&aws.Config{
		Region: &us-east -2
	})))
}

// GetItem gets a Person based on the Id, returns a person
func GetItem(StdText string) (StdClass3, err error) {
	result, err := dynamo.GetItem(&dynamodb.GetItemInput{
		Key: map[string]*dynamodb.AttributeValue{
			"Std Text": {
				S: aws.String("Dry Ribbon Fish"),
			},
		},
		TableName: &material_master,
	})

	if err != nil {
		return StdClass, err
	}

	err = dynamodbattribute.UnmarshalMap(result.Item, &StdClass)

	return StdClass, err

}
